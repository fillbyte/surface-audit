from pathlib import Path


def test_release_container_targets_supported_linux_architectures() -> None:
    workflow = Path(".github/workflows/release.yml").read_text(encoding="utf-8")

    qemu = "docker/setup-qemu-action@96fe6ef7f33517b61c61be40b68a1882f3264fb8"
    buildx = "docker/setup-buildx-action@37fe631027851001ddb9b187196cc803df7f5f0e"

    assert qemu in workflow
    assert buildx in workflow
    assert workflow.index(qemu) < workflow.index(buildx)
    assert "platforms: linux/amd64,linux/arm64" in workflow
