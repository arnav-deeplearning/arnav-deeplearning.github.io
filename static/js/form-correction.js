import {
  FilesetResolver,
  PoseLandmarker,
  DrawingUtils,
} from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@1.0.1/vision_bundle.mjs";

// Pinned CDN version so a future MediaPipe release can't silently break
// this page. WASM runtime + model both load fresh from Google's CDN --
// nothing bundled, nothing self-hosted, and everything runs client-side.
const WASM_URL = "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@1.0.1/wasm";
const MODEL_URL = "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task";

// BlazePose 33-point topology (standard across MediaPipe Pose releases).
// Exported (along with the pure geometry/check functions below) so they
// can be unit-tested with synthetic landmark data via dynamic import --
// there's no way to test real pose accuracy without an actual camera and
// a human in frame, but the angle/threshold math itself is fully testable.
export const LM = {
  LEFT_SHOULDER: 11, RIGHT_SHOULDER: 12,
  LEFT_ELBOW: 13, RIGHT_ELBOW: 14,
  LEFT_WRIST: 15, RIGHT_WRIST: 16,
  LEFT_HIP: 23, RIGHT_HIP: 24,
  LEFT_KNEE: 25, RIGHT_KNEE: 26,
  LEFT_ANKLE: 27, RIGHT_ANKLE: 28,
};

export function angleAt(a, vertex, c) {
  const v1 = { x: a.x - vertex.x, y: a.y - vertex.y, z: (a.z || 0) - (vertex.z || 0) };
  const v2 = { x: c.x - vertex.x, y: c.y - vertex.y, z: (c.z || 0) - (vertex.z || 0) };
  const mag1 = Math.hypot(v1.x, v1.y, v1.z);
  const mag2 = Math.hypot(v2.x, v2.y, v2.z);
  if (mag1 === 0 || mag2 === 0) return null;
  const dot = v1.x * v2.x + v1.y * v2.y + v1.z * v2.z;
  const cos = Math.max(-1, Math.min(1, dot / (mag1 * mag2)));
  return (Math.acos(cos) * 180) / Math.PI;
}

export function distance(a, b) {
  return Math.hypot(a.x - b.x, a.y - b.y, (a.z || 0) - (b.z || 0));
}

// Computes the geometric metrics every check is evaluated against.
// Angles/distances use MediaPipe's 3D world landmarks (real-world
// meters, camera-distance independent); the guard-up check uses the
// 2D image landmarks instead, since "above/below" on screen is exactly
// what normalized image-space y already gives us unambiguously.
export function computeMetrics(world, image) {
  const leftKnee = angleAt(world[LM.LEFT_HIP], world[LM.LEFT_KNEE], world[LM.LEFT_ANKLE]);
  const rightKnee = angleAt(world[LM.RIGHT_HIP], world[LM.RIGHT_KNEE], world[LM.RIGHT_ANKLE]);
  const shoulderWidth = distance(world[LM.LEFT_SHOULDER], world[LM.RIGHT_SHOULDER]);
  const ankleWidth = distance(world[LM.LEFT_ANKLE], world[LM.RIGHT_ANKLE]);
  const ratio = shoulderWidth > 0.001 ? ankleWidth / shoulderWidth : null;

  const shoulderY = (image[LM.LEFT_SHOULDER].y + image[LM.RIGHT_SHOULDER].y) / 2;
  const hipY = (image[LM.LEFT_HIP].y + image[LM.RIGHT_HIP].y) / 2;
  const midY = (shoulderY + hipY) / 2;
  const guardUp = image[LM.LEFT_WRIST].y < midY || image[LM.RIGHT_WRIST].y < midY;

  return { leftKnee, rightKnee, shoulderWidth, ankleWidth, ratio, guardUp };
}

// Widens/narrows a [min, max] range around its center by `factor` --
// this is how the Beginner/Standard/Strict sensitivity control works,
// applied uniformly to every range-shaped check.
export function adjustedRange(check, factor) {
  const center = (check.min + check.max) / 2;
  const halfWidth = ((check.max - check.min) / 2) * factor;
  return [center - halfWidth, center + halfWidth];
}

export const CHECK_HANDLERS = {
  min_knee_bend: (check, m, factor) => {
    const [min, max] = adjustedRange(check, factor);
    const bent = Math.min(m.leftKnee, m.rightKnee);
    return bent >= min && bent <= max;
  },
  max_knee_straight: (check, m, factor) => {
    const [min, max] = adjustedRange(check, factor);
    const straight = Math.max(m.leftKnee, m.rightKnee);
    return straight >= min && straight <= max;
  },
  both_knees_range: (check, m, factor) => {
    const [min, max] = adjustedRange(check, factor);
    return m.leftKnee >= min && m.leftKnee <= max && m.rightKnee >= min && m.rightKnee <= max;
  },
  knee_symmetry_close: (check, m, factor) => {
    const [, max] = adjustedRange(check, factor);
    return Math.abs(m.leftKnee - m.rightKnee) <= max;
  },
  knee_symmetry_apart: (check, m, factor) => {
    const [min] = adjustedRange(check, factor);
    return Math.abs(m.leftKnee - m.rightKnee) >= min;
  },
  ankle_shoulder_ratio: (check, m, factor) => {
    if (m.ratio === null) return { pass: false, direction: null };
    const [min, max] = adjustedRange(check, factor);
    if (m.ratio < min) return { pass: false, direction: "low" };
    if (m.ratio > max) return { pass: false, direction: "high" };
    return { pass: true, direction: null };
  },
  guard_up: (check, m) => m.guardUp,
};

export function evaluateCheck(check, metrics, sensitivityFactor) {
  const result = CHECK_HANDLERS[check.kind](check, metrics, sensitivityFactor);
  if (typeof result === "boolean") {
    return { pass: result, message: result ? check.feedback_ok : check.feedback_bad };
  }
  // ankle_shoulder_ratio shape: { pass, direction }
  if (result.pass) return { pass: true, message: check.feedback_ok };
  const message = result.direction === "high" ? check.feedback_high : check.feedback_low;
  return { pass: false, message };
}

(() => {
  const el = {
    stanceSelect: document.getElementById("stanceSelect"),
    sensitivitySelect: document.getElementById("sensitivitySelect"),
    stanceDescription: document.getElementById("stanceDescription"),
    audioToggle: document.getElementById("audioToggle"),
    skeletonToggle: document.getElementById("skeletonToggle"),
    startCameraBtn: document.getElementById("startCameraBtn"),
    stopCameraBtn: document.getElementById("stopCameraBtn"),
    statusMessage: document.getElementById("statusMessage"),
    cameraStage: document.getElementById("cameraStage"),
    video: document.getElementById("video"),
    canvas: document.getElementById("overlay"),
    feedbackPanel: document.getElementById("feedbackPanel"),
  };

  if (!el.stanceSelect) return; // not on the form-correction page

  let stances = [];
  let poseLandmarker = null;
  let stream = null;
  let running = false;
  let lastVideoTime = -1;
  let lastSpoken = "";
  let lastSpokenAt = 0;

  const ctx = el.canvas.getContext("2d");
  const drawingUtils = new DrawingUtils(ctx);

  function currentStance() {
    return stances.find((s) => s.id === el.stanceSelect.value) || stances[0];
  }

  function updateStanceDescription() {
    const stance = currentStance();
    el.stanceDescription.textContent = stance ? stance.description : "";
  }

  async function initModel() {
    const vision = await FilesetResolver.forVisionTasks(WASM_URL);
    try {
      poseLandmarker = await PoseLandmarker.createFromOptions(vision, {
        baseOptions: { modelAssetPath: MODEL_URL, delegate: "GPU" },
        runningMode: "VIDEO",
        numPoses: 1,
      });
    } catch {
      // Some browsers/devices don't support the GPU delegate -- fall back to CPU.
      poseLandmarker = await PoseLandmarker.createFromOptions(vision, {
        baseOptions: { modelAssetPath: MODEL_URL, delegate: "CPU" },
        runningMode: "VIDEO",
        numPoses: 1,
      });
    }
  }

  function resizeCanvas() {
    el.canvas.width = el.video.videoWidth;
    el.canvas.height = el.video.videoHeight;
  }

  function speak(message) {
    if (!el.audioToggle.checked || !message || !("speechSynthesis" in window)) return;
    const now = Date.now();
    if (now - lastSpokenAt < 2500) return;
    if (message === lastSpoken && now - lastSpokenAt < 6000) return;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(new SpeechSynthesisUtterance(message));
    lastSpoken = message;
    lastSpokenAt = now;
  }

  function renderFeedback(checkResults, personDetected) {
    el.feedbackPanel.innerHTML = "";

    if (!personDetected) {
      const p = document.createElement("p");
      p.className = "muted";
      p.style.textAlign = "center";
      p.textContent = "No person detected — step into frame, a few steps back from the camera.";
      el.feedbackPanel.appendChild(p);
      return;
    }

    let firstFailMessage = null;
    checkResults.forEach(({ check, pass, message }) => {
      const row = document.createElement("div");
      row.className = `feedback-row feedback-${pass ? "pass" : "fail"}`;
      row.innerHTML = `
        <span class="feedback-icon">${pass ? "✓" : "✕"}</span>
        <span class="feedback-text"><strong>${check.label}</strong><br>${message}</span>
      `;
      el.feedbackPanel.appendChild(row);
      if (!pass && !firstFailMessage) firstFailMessage = message;
    });

    speak(firstFailMessage || "Great form — keep it up.");
  }

  function processResult(result) {
    if (el.skeletonToggle.checked) {
      ctx.save();
      ctx.clearRect(0, 0, el.canvas.width, el.canvas.height);
      if (result.landmarks && result.landmarks.length > 0) {
        drawingUtils.drawLandmarks(result.landmarks[0], { radius: 3 });
        drawingUtils.drawConnectors(result.landmarks[0], PoseLandmarker.POSE_CONNECTIONS);
      }
      ctx.restore();
    } else {
      ctx.clearRect(0, 0, el.canvas.width, el.canvas.height);
    }

    if (!result.landmarks || result.landmarks.length === 0) {
      renderFeedback([], false);
      return;
    }

    const metrics = computeMetrics(result.worldLandmarks[0], result.landmarks[0]);
    const sensitivityFactor = parseFloat(el.sensitivitySelect.value);
    const stance = currentStance();
    const checkResults = stance.checks.map((check) => ({
      check,
      ...evaluateCheck(check, metrics, sensitivityFactor),
    }));
    renderFeedback(checkResults, true);
  }

  function renderLoop() {
    if (!running) return;
    if (el.video.currentTime !== lastVideoTime) {
      lastVideoTime = el.video.currentTime;
      const result = poseLandmarker.detectForVideo(el.video, performance.now());
      processResult(result);
    }
    requestAnimationFrame(renderLoop);
  }

  async function startCamera() {
    el.startCameraBtn.disabled = true;
    try {
      if (!poseLandmarker) {
        el.statusMessage.textContent = "Loading pose model (first time only)…";
        await initModel();
      }
      el.statusMessage.textContent = "Requesting camera access…";
      stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" }, audio: false });
      el.video.srcObject = stream;
      await el.video.play();
      resizeCanvas();

      el.cameraStage.style.display = "";
      el.feedbackPanel.style.display = "";
      el.startCameraBtn.style.display = "none";
      el.stopCameraBtn.style.display = "";
      el.statusMessage.textContent = "";
      running = true;
      renderLoop();
    } catch (err) {
      handleError(err);
    } finally {
      el.startCameraBtn.disabled = false;
    }
  }

  function stopCamera() {
    running = false;
    if (stream) {
      stream.getTracks().forEach((track) => track.stop());
      stream = null;
    }
    el.video.srcObject = null;
    window.speechSynthesis && window.speechSynthesis.cancel();
    el.cameraStage.style.display = "none";
    el.feedbackPanel.style.display = "none";
    el.startCameraBtn.style.display = "";
    el.stopCameraBtn.style.display = "none";
    el.statusMessage.textContent = 'Click "Start Camera" to begin.';
  }

  function handleError(err) {
    let message;
    if (err && (err.name === "NotAllowedError" || err.name === "PermissionDeniedError")) {
      message = "Camera access was denied. Allow camera access in your browser's site settings and try again.";
    } else if (err && (err.name === "NotFoundError" || err.name === "DevicesNotFoundError")) {
      message = "No camera was found on this device.";
    } else if (err && err.name === "NotReadableError") {
      message = "Your camera is busy or unavailable — close any other app using it and try again.";
    } else {
      message = "Something went wrong loading the pose model or camera. A slow or blocked connection to the model CDN is the most common cause — check your connection and try again.";
    }
    el.statusMessage.textContent = message;
  }

  el.stanceSelect.addEventListener("change", updateStanceDescription);
  el.startCameraBtn.addEventListener("click", startCamera);
  el.stopCameraBtn.addEventListener("click", stopCamera);
  window.addEventListener("beforeunload", stopCamera);

  const embedded = document.getElementById("form-correction-data");
  if (embedded) {
    try {
      stances = JSON.parse(embedded.textContent).stances || [];
    } catch {
      stances = [];
    }
  }
  updateStanceDescription();

  // Lets the plain inline script in form-correction.html know the module
  // actually loaded and ran, so it can tell the difference between "still
  // loading" and "silently failed" and only warn the user in the latter case.
  window.__formCorrectionModuleLoaded = true;
})();
