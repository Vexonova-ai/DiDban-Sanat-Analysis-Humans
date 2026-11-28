# Engineering ownership and acceptance

Shared contracts are in src/core. All engineers use synthetic tests first, respect
BGR/original-frame conventions, avoid import-time model downloads, and coordinate
breaking changes through a dedicated approved PR. Feature files below are future
targets, not Phase 0 implementations. Branches are reserved, not pre-created.

## Role 01 - Person Detection

- Branch: feature/detection. Ownership: src/detection/.
- Files/classes: video_reader.py / VideoReader; preprocessor.py / FramePreprocessor;
  person_detector.py / PersonDetector; person_cropper.py / PersonCropper;
  stage.py / DetectionStage.
- Input: authorized video and configuration, then FrameData.
- Output: DetectionPacket, including packets with no detections.
- Dependencies: core schemas and IPersonDetector, OpenCV, NumPy, Ultralytics/PyTorch.
- Implement decoding, frame preparation, person-only inference, coordinate restoration,
  crop extraction and packet assembly. Own detector model loading and error handling.
- Tests: empty/invalid video, end-of-stream, resize mapping, clipped/exclusive boxes,
  BGR uint8 crops, confidence and empty detections; use injected model fakes in CI.
- Acceptance: ordered packets preserve original frames, IDs, timestamps and valid
  coordinates; resources close on success/failure. Verify weights and license separately.
- Boundary: do not own tracking, buffering, fashion, worker orchestration or storage.

## Role 02 - Tracking, ReID and Buffer

- Branch: feature/tracking-reid. Ownership: src/tracking/ and src/buffer/.
- Files/classes: tracking/person_tracker.py / PersonTracker;
  tracking/reid_model.py / ReIDModel; tracking/identity_manager.py / IdentityManager;
  buffer/person_buffer.py / PersonBuffer; buffer/quality_selector.py / QualitySelector.
- Input: DetectionPacket; intermediate TrackedPerson. Output: ConfirmedPerson or None.
- Dependencies: core IPersonTracker/IPersonBuffer, Role 01 packet contract; select and
  justify ByteTrack and OSNet packages, pretrained provenance and licenses.
- Implement tracker adapter, appearance embedding adapter, session identity association,
  valid-observation buffering and source-crop selection. ByteTrack has no native OSNet
  integration assumption. Define explicit session reset with integration.
- Tests: empty frames, track loss/reappearance, identity association, distinct-frame
  counting, non-consecutive observations, fifteenth observation, duplicate confirmations,
  expiration and reset. Keep model tests separate from deterministic algorithm tests.
- Acceptance: one confirmation per anonymous session identity, no duplicate after buffer
  expiration, correct selected-frame provenance, agreed quality and expiration rules.
- Boundary: no persistent cross-video identity database, detection, fashion or queues.

## Role 03 - Fashion Recognition

- Branch: feature/fashion. Ownership: src/fashion/.
- Files/classes: fashion_model.py / FashionModel; mask_extractor.py / MaskExtractor;
  attribute_extractor.py / AttributeExtractor.
- Input: ConfirmedPerson. Output: FashionResult.
- Dependencies: IFashionModel, PyTorch, Transformers, Pillow and verified SegFormer model.
- Implement model loading, explicit BGR/RGB conversion, inference, mask resizing and
  verified-label extraction. Propose an attribute schema with storage/integration.
- Tests: input convention, model failure, label mapping, nearest-neighbor mask alignment,
  Boolean masks and source identity/frame preservation; mock models for infrastructure CI.
- Acceptance: masks match selected crop dimensions; unsupported clothing categories are
  not invented; provenance, licensing and actual model compatibility are documented.
- Boundary: no tracking, confirmation logic, persistence or worker lifecycle management.

## Role 04 - Pipeline and Integration

- Branch: feature/pipeline. Ownership: src/pipeline/ and future application entry point.
- Files/classes: workers.py / DetectionWorker, TrackingWorker, FashionWorker;
  pipeline_manager.py / PipelineManager. Own future main.py.
- Input: configuration/video plus injected feature implementations. Output: coordinated
  contract delivery, results, lifecycle status and propagated failures.
- Dependencies: Roles 01-03 ABCs and Role 05 storage API; agree reset and error protocols.
- Implement a validated sequential application first, then three application workers
  and two bounded queues. Include backpressure, ordering, shutdown and resource cleanup.
- Tests: deterministic sequential integration, empty video, worker exceptions, full queues,
  cancellation, end-of-stream, reset and shutdown without deadlocks or lost failures.
- Acceptance: ordered, memory-conscious processing and evidence of safe lifecycle behavior.
  Full annotated video requires original frames and tracking metadata, not just ConfirmedPerson.
- Boundary: orchestrate adapters; do not duplicate their inference or storage algorithms.

## Role 05 - Storage and Evaluation

- Branch: feature/storage-evaluation. Ownership: src/storage/.
- Files/classes: repository.py / DataStorage; mask_storage.py / MaskStorage;
  renderer.py / VideoRenderer; evaluator.py / Evaluator.
- Input: FashionResult plus agreed crop/original-frame and tracking metadata for rendering.
- Output: structured records, masks, supported visual outputs and evaluation metrics.
- Dependencies: core schemas/exceptions, Role 03 attribute agreement and Role 04 frame access.
- Implement JSON persistence, masks, rendering and performance/evaluation reporting with
  explicit session isolation, error handling, retention and output naming policies.
- Tests: serialization, Unicode-safe paths, failed writes, mask round trips, missing frame
  context, rendering alignment, deterministic metrics and authorized end-to-end samples.
- Acceptance: stored outputs preserve IDs/frame provenance; visual claims match available
  inputs; report measured metrics without treating synthetic fixtures as accuracy evidence.
- Boundary: no model inference, identity association, buffer policy or queue orchestration.
