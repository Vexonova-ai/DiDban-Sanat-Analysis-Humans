"""Canned boundary interoperability, not a production application pipeline."""

from src.core.schemas import DetectionPacket
from tests.fixtures.fakes import FakeBuffer, FakeDetector, FakeFashionModel, FakeTracker


def test_canned_contract_exchange(contracts: tuple) -> None:
    frame, detection, _, tracked, person, result = contracts
    packet = DetectionPacket(frame, FakeDetector([detection]).detect(frame))
    observation = FakeTracker([tracked]).update(packet)[0]
    assert FakeBuffer(None).update(observation) is None
    confirmation = FakeBuffer(person).update(observation)
    assert confirmation is person
    output = FakeFashionModel(result).predict(confirmation)
    assert output is result
    assert output.frame_id == confirmation.frame_id
    assert output.person_id == confirmation.person_id
