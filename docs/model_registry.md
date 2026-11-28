# Initial model candidates

No weights were downloaded or pretrained models executed in Phase 0.

| Purpose | Candidate | Initial settings | Owner |
| --- | --- | --- | --- |
| Detection | YOLOv8, yolov8n.pt | Person, size 640, Ultralytics/PyTorch | Role 01 |
| Tracking | ByteTrack | Backend and thresholds pending | Role 02 |
| Appearance ReID | OSNet, osnet_x1_0 | Anonymous association within one video session | Role 02 |
| Human parsing | SegFormer B2, mattmdjaga/segformer_b2_clothes | PyTorch/Transformers; pretrained inference without custom training | Role 03 |

Standard ByteTrack does not natively integrate OSNet. Role 02 must select and validate
that integration; Phase 0 installs no arbitrary tracking or ReID backend.

The [SegFormer model card](https://huggingface.co/mattmdjaga/segformer_b2_clothes)
describes ATR-based parsing and declares an `other` license. Review the specific
license and dataset terms before deployment. Do not assume support for arbitrary
garments, materials, colors or industrial PPE. Role 03 must verify the checkpoint
label mapping, processor, revision, resolution and crop alignment. Occlusion, small
crops, illumination and domain shift require evaluation with authorized data.

Engineers must record provenance, revision/hash, redistribution rights, model and
software licenses, preprocessing, supported categories, dependency compatibility
and measured hardware requirements. The repository MIT license does not grant
third-party model or dataset rights. Review Ultralytics/YOLO licensing for the intended
deployment. ReID provenance, license, retention and association quality are pending.

Inference must stay local. Human parsing is segmentation; a face segmentation class
is not facial recognition. Do not implement facial recognition or persistent cross-video
identities. Restrict access, minimize retention and obtain appropriate authorization
for sensitive video. Keep recordings, embeddings and results out of Git. Phase 0 adds
no telemetry or cloud transmission. Review third-party runtime settings before models
are loaded in future work.
