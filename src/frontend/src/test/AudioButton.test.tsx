import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, fireEvent, act } from "@testing-library/react";
import AudioButton from "../components/AudioButton";

vi.mock("react-i18next", () => ({
  useTranslation: () => ({
    t: (key: string) => key,
    i18n: { language: "en", changeLanguage: vi.fn() },
  }),
}));

const markListenedMock = vi.fn().mockResolvedValue(undefined);
vi.mock("../services/api", () => ({
  markListened: (...args: unknown[]) => markListenedMock(...args),
}));

class MockAudio {
  static instances: MockAudio[] = [];

  public currentTime = 0;
  public preload = "";
  public oncanplay: (() => void) | null = null;
  public onended: (() => void) | null = null;
  public onerror: (() => void) | null = null;
  public readonly play = vi.fn().mockResolvedValue(undefined);
  public readonly pause = vi.fn();
  public readonly load = vi.fn();

  constructor(public readonly src: string) {
    MockAudio.instances.push(this);
  }
}

describe("AudioButton", () => {
  beforeEach(() => {
    MockAudio.instances = [];
    markListenedMock.mockClear();
    vi.useFakeTimers();
    vi.spyOn(globalThis, "setTimeout");
    vi.stubGlobal("Audio", MockAudio as unknown as typeof Audio);
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("preloads example audio and keeps word-to-example break within the 1s budget", async () => {
    render(
      <AudioButton
        wordId="w1"
        wordText="ciao"
        token="token"
        hasExample
      />
    );

    await act(async () => {
      fireEvent.click(screen.getByRole("button"));
    });

    expect(MockAudio.instances).toHaveLength(2);
    const wordAudio = MockAudio.instances.find((a) => !a.src.includes("/example"));
    const exampleAudio = MockAudio.instances.find((a) => a.src.includes("/example"));
    expect(wordAudio).toBeDefined();
    expect(exampleAudio).toBeDefined();

    await act(async () => {
      exampleAudio?.oncanplay?.();
      wordAudio?.onended?.();
    });

    await Promise.resolve();
    expect(globalThis.setTimeout).toHaveBeenCalledWith(expect.any(Function), 250);

    await act(async () => {
      await vi.advanceTimersByTimeAsync(249);
    });
    expect(exampleAudio?.play).not.toHaveBeenCalled();

    await act(async () => {
      await vi.advanceTimersByTimeAsync(1);
    });
    expect(globalThis.setTimeout).toHaveBeenCalledWith(expect.any(Function), 750);
    expect(exampleAudio?.play).toHaveBeenCalledTimes(1);

    await act(async () => {
      exampleAudio?.onended?.();
    });
    await Promise.resolve();
    expect(markListenedMock).toHaveBeenCalledWith("w1");
  });
});
