# Shared data contracts

The source of truth is `src/core/schemas.py`; interfaces are in `src/core/interfaces.py`.
These are passive dataclasses. Annotations do not validate, freeze, copy, or serialize
data. Producers must enforce conventions in future implementations.

| Contract | Meaning |
| --- | --- |
| FrameData | Original image, zero-based frame ID and timestamp in seconds |
| Detection | Original-frame bbox, confidence and person crop |
| DetectionPacket | Frame and possibly empty detections |
| TrackedPerson | Frame, timestamp, tracker ID, session person ID, bbox and crop |
| ConfirmedPerson | Session person ID, selected frame/timestamp, valid count, bbox and image |
| FashionResult | Matching person/frame IDs, masks and attributes |

Images use OpenCV BGR order, NumPy uint8 and height x width x 3 shape. Model adapters
must explicitly convert to RGB when needed. Bounding boxes are integer xyxy in the
original video frame. Right and bottom boundaries are exclusive: width = x2 - x1,
height = y2 - y1. Producers must clip and reject invalid boxes and transform resized
detector coordinates back to original-frame coordinates.

Confidence ranges from zero to one. Frame IDs start at zero. Timestamps are seconds.
track_id comes from the tracker; person_id is anonymous and scoped to one video session.
Masks are two-dimensional Boolean NumPy arrays matching the selected crop dimensions.
Fashion results must correspond to the selected source image and frame, which can
differ from the frame that triggers confirmation. Detailed attributes remain unspecified.

Published arrays must not be mutated after worker transfer. Copy or explicitly
transfer ownership; dataclasses do not enforce this. Session isolation and reset
are external responsibilities because the exact contracts contain no session field.
Full annotated-video output requires original frames and tracking metadata beyond
ConfirmedPerson and FashionResult.

- IPersonDetector.detect(FrameData) returns list[Detection].
- IPersonTracker.update(DetectionPacket) returns list[TrackedPerson].
- IPersonBuffer.update(TrackedPerson) returns ConfirmedPerson or None.
- IFashionModel.predict(ConfirmedPerson) returns FashionResult.

Breaking field or signature changes require a dedicated PR and project leader approval.
Reset, lifecycle, and detailed attribute schemas remain engineering design decisions.
