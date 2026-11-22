import numpy as np
import matplotlib.pyplot as plt

# ---------------- ADC and sampling checks ----------------
BITS = 10
VREF = 5.0

def check_adc_basics(step_size, volts_for_512):
    """Check the two answers from 'the ADC: voltage in, number out'."""
    if step_size is None or volts_for_512 is None:
        print("⏳ Fill in both answers first.")
        return

    true_step = VREF / 2 ** BITS        # volts per step
    true_512 = 512 * true_step          # volts for a reading of 512

    # 1) step size (accept anything within 5 %)
    if abs(step_size - true_step) / true_step < 0.05:
        print("✅ Step size: correct.")
    elif step_size > 0.1:
        print("❌ Step size: that's very large for one step. Is your answer in volts or millivolts?")
    else:
        print("❌ Step size: not quite. Hint: split the whole range (0 to 5 V) into 1024 equal steps.")

    # 2) volts for a count of 512
    if abs(volts_for_512 - true_512) < 0.05:
        print("✅ 512 counts: correct.")
    else:
        print("❌ 512 counts: not quite. Hint: where is 512 in the range 0 to 1023?")

def check_sampling_basics(spacing, duration):
    """Check the two answers from 'sampling: how often do we measure?'."""
    if spacing is None or duration is None:
        print("⏳ Fill in both answers first.")
        return

    true_spacing = 1 / 250          # seconds between samples
    true_duration = 500 / 250       # seconds for 500 samples

    if abs(spacing - true_spacing) / true_spacing < 0.01:
        print("✅ Time between samples: correct.")
    elif spacing > 0.5:
        print("❌ Time between samples: that's way too long. Check your units (samples per SECOND).")
    else:
        print("❌ Time between samples: not quite. Hint: 250 samples fit into 1 second. How long is each one?")

    if abs(duration - true_duration) < 0.01:
        print("✅ Recording length: correct.")
    elif duration > 100:
        print("❌ Recording length: that's over a minute for a short recording. Check the units: samples ÷ (samples per second).")
    else:
        print("❌ Recording length: not quite. Hint: number of samples × time per sample.")


# ---------------- calculator tests ----------------
import contextlib, io

def _describe_call(calculate, *args):
    """Run calculate(*args) and describe, in words, what happened."""
    printed_text = io.StringIO()
    try:
        with contextlib.redirect_stdout(printed_text):
            result = calculate(*args)
        said = printed_text.getvalue().strip()
        text = f"returned {result!r}"
        if said:
            text += f" and printed {said!r}"
        return text
    except ZeroDivisionError as error:
        return f"crashed with Python's own ZeroDivisionError ({error})"
    except Exception as error:
        return f"raised {type(error).__name__}({str(error)!r})"


def test_calculate(calculate):
    """Run the tests on your calculate() function."""
    if calculate is None:
        print("⏳ Write (or paste) your calculate function first.")
        return

    cases = [
        ((6, 3, "add"), 9),
        ((6, 3, "subtract"), 3),
        ((6, 3, "multiply"), 18),
        ((6, 3, "divide"), 2),
        ((5, 0, "add"), 5),
        ((5, 0, "multiply"), 0),
        ((0, 5, "divide"), 0),
        ((-2, 3, "multiply"), -6),
    ]
    passed = 0
    for args, expected in cases:
        try:
            got = calculate(*args)
        except Exception as error:
            got = f"error: {type(error).__name__}"
        if got == expected:
            passed += 1
            print(f"✅ calculate{args} = {got}")
        else:
            print(f"❌ calculate{args}: expected {expected}, got {got!r}")
    print(f"\n{passed} of {len(cases)} normal and zero cases passed.")

    print("\nError cases: there's no ✅ or ❌ here. Is this what YOU wanted?")
    for args in [(5, 0, "divide"), (5, 3, "power")]:
        print(f"  calculate{args} -> {_describe_call(calculate, *args)}")


# ---------------- prime tests ----------------
def test_is_prime(is_prime):
    """Run the tests on your is_prime(n) function."""
    if is_prime is None:
        print("⏳ Write your is_prime function first.")
        return

    def says_prime(n):
        try:
            return bool(is_prime(n))
        except Exception:
            return False

    def crashed(n):
        try:
            is_prime(n)
            return False
        except Exception:
            return True

    known_below_30 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    found = [n for n in range(0, 30) if says_prime(n)]
    wrongly = [n for n in found if n not in known_below_30]
    missed = [n for n in known_below_30 if n not in found]
    crashes = [n for n in range(0, 30) if crashed(n)]

    # 1) the primes below 30
    if found == known_below_30:
        print("✅ Primes below 30: correct.")
    else:
        print("❌ Primes below 30: not quite.")
        if wrongly:
            print(f"     It says these are prime, but they aren't: {wrongly}")
        if missed:
            print(f"     It misses these primes: {missed}")
        if crashes:
            print(f"     It crashes on: {crashes}")

    # 2) how many primes below 100
    count = sum(1 for n in range(0, 100) if says_prime(n))
    if count == 25:
        print("✅ Primes below 100: 25, correct.")
    else:
        print(f"❌ Primes below 100: your function finds {count}. Is that what you expected?")

    # 3) awkward inputs
    awkward = {0: False, 1: False, -7: False}
    bad = [n for n, want in awkward.items() if says_prime(n) != want]
    if not bad:
        print("✅ 0, 1 and a negative number: correctly not prime.")
    else:
        print(f"❌ Awkward inputs: it says these are prime, but they aren't: {bad}")


# ---------------- Part 1 checks ----------------
def check_part1_predictions(baseline_guess, beats_guess):
    """Check the two predictions at the start of Part 1."""
    if baseline_guess is None or beats_guess is None:
        print("⏳ Fill in both predictions first.")
        return

    # 1) resting level: 2.5 V is the middle of 0 to 5 V, which is count 512 (accept +/- 32)
    middle = 2 ** BITS // 2
    if abs(baseline_guess - middle) <= 32:
        print("✅ Resting level: correct.")
    elif 0 <= baseline_guess < 6:
        print("❌ Resting level: that looks like volts. We want a count, between 0 and 1023.")
    else:
        print("❌ Resting level: not quite. Hint: the signal rests at 2.5 V. Which count is that?")

    # 2) beats in 2 seconds: 60 to 100 beats per minute is about 2 to 3 beats in 2 seconds
    if 2 <= beats_guess <= 3.5:
        print("✅ Beats in 2 seconds: correct.")
    elif beats_guess < 2:
        print("❌ Beats in 2 seconds: too few. 60 beats a minute is 1 beat every second.")
    else:
        print("❌ Beats in 2 seconds: too many. Remember, that's beats per MINUTE, and we only record for 2 seconds.")


# ---------------- Part 2 and 3 checks ----------------
def check_time_predictions(spacing, last_time):
    """Check the two hand calculations at the start of Part 2."""
    if spacing is None or last_time is None:
        print("⏳ Fill in both answers first.")
        return

    # 1) the gap between samples
    true_spacing = 1 / 250
    if abs(spacing - true_spacing) / true_spacing < 0.01:
        print("✅ Time between samples: correct.")
    elif spacing > 0.5:
        print("❌ Time between samples: that's way too long. Check your units (samples per SECOND).")
    else:
        print("❌ Time between samples: not quite. Hint: 250 samples fit into 1 second.")

    # 2) the time of the last sample
    true_last = 499 / 250
    if abs(last_time - true_last) < 0.0005:
        print("✅ Last sample: correct.")
    elif abs(last_time - 2.0) < 0.0005:
        print("❌ Last sample: 2.0 s is how long the whole recording lasts. But the first sample is at t = 0, so when is the 500th?")
    elif last_time > 100:
        print("❌ Last sample: that's way too long. Check your units.")
    else:
        print("❌ Last sample: not quite. Hint: the first sample is at t = 0. How many gaps are there between 500 samples?")


def check_time_axis(t, expected_spacing, expected_last_time):
    """Compare the time axis you built with the numbers you worked out by hand."""
    if t is None:
        print("⏳ Build t first.")
        return
    if expected_spacing is None or expected_last_time is None:
        print("⏳ Fill in your two hand-worked answers first.")
        return
    try:
        t = np.asarray(t, dtype=float)
        first, spacing, last = t[0], t[1] - t[0], t[-1]
    except Exception:
        print("❌ t should be an array of times, one per sample. Did your code give back numbers?")
        return

    print(f"first sample:  {first:.6f} s  (should be 0)")
    print(f"spacing:       {spacing:.6f} s  (you expected {expected_spacing:.6f})")
    print(f"last sample:   {last:.6f} s  (you expected {expected_last_time:.6f})")

    ok = (np.isclose(first, 0)
          and np.allclose(np.diff(t), expected_spacing)
          and np.isclose(last, expected_last_time))
    if ok:
        print("✅ Your code matches your hand calculation.")
    else:
        print("❌ Mismatch. Either the code or your calculation is wrong. Which one?")



def check_counts_to_volts(fn):
    """Test your counts_to_volts function on the 2.000 V reference (channel 2)."""
    try:
        cal = SimulatedDAQ(seed=42).read_adc(channel=2, n_samples=200, fs=250)        
        v = fn(cal)
    except Exception as error:
        print(f"❌ Your function crashed: {type(error).__name__}: {error}")
        return
    if v is None:
        print("⏳ Your function doesn't give anything back yet. Does it `return` the volts?")
        return
    try:
        v = np.asarray(v, dtype=float)
    except Exception:
        print("❌ Your function should return numbers (volts).")
        return
    if v.shape != cal.shape:
        print(f"❌ It should return one voltage for each count ({len(cal)} values), but it returned something of shape {v.shape}.")
        return
    mean_v = v.mean()
    if abs(mean_v - 2.000) < 0.01:
        print(f"✅ Channel 2 reads {mean_v:.3f} V (expected 2.000 V).")
    else:
        print(f"❌ Channel 2 reads {mean_v:.3f} V, but the reference is exactly 2.000 V. Hint: check the range and the number of steps you used.")


# ---------------- Part 5 checks ----------------
def _hum_size(x, fs):
    """Size (volts) of the 50 Hz component in x."""
    x = np.asarray(x, dtype=float)
    n = np.arange(len(x))
    return 2 * abs(np.mean((x - x.mean()) * np.exp(-2j * np.pi * 50 * n / fs)))

def _r_height(x):
    """Height of the tallest spike above the flat parts (the median).
    The first and last 25 samples (0.1 s) are skipped: filters misbehave at the edges."""
    x = np.asarray(x, dtype=float)
    return x[25:-25].max() - np.median(x)

def check_hum_removal(fn, volts, fs):
    """Run your remove_hum function and check the two things we decided in the plan."""
    try:
        out = fn(volts, fs)
    except Exception as error:
        print(f"❌ Your function crashed: {type(error).__name__}: {error}")
        return
    if out is None:
        print("⏳ Your function doesn't give anything back yet. Does it `return` the filtered signal?")
        return
    try:
        out = np.asarray(out, dtype=float)
    except Exception:
        print("❌ Your function should return the filtered signal (an array of volts).")
        return
    if out.shape != np.shape(volts):
        print(f"❌ It should return one value per sample ({len(volts)}), but it returned something of shape {out.shape}.")
        return

    hum_before, hum_after = _hum_size(volts, fs), _hum_size(out, fs)
    r_before, r_after = _r_height(volts), _r_height(out)
    print(f"50 Hz hum:     {hum_before:.3f} V before, {hum_after:.3f} V after")
    print(f"R-wave height: {r_before:.2f} V before, {r_after:.2f} V after")

    hum_ok = hum_after < 0.3 * hum_before
    r_ok = abs(r_after - r_before) < 0.25 * r_before
    if hum_ok and r_ok:
        print("✅ The hum is gone and the R wave is still as tall.")
    elif r_ok:
        print("❌ The R wave is fine, but the 50 Hz hum is still there.")
    elif hum_ok:
        print("❌ The hum is gone, but the R wave has changed height. That's part of the heart's signal, not noise.")
    else:
        print("❌ The hum is still there, and the R wave has changed height.")


# ---------------- Part 6 checks ----------------
def check_heart_rate(fn, signal, fs, bpm_by_hand):
    """Run your heart_rate function and check it against the two things we decided in the plan."""
    if bpm_by_hand is None:
        print("⏳ Fill in your by-hand answer first.")
        return
    try:
        bpm = fn(signal, fs)
    except Exception as error:
        print(f"❌ Your function crashed: {type(error).__name__}: {error}")
        return
    if bpm is None:
        print("⏳ Your function doesn't give anything back yet. Does it `return` the heart rate?")
        return
    try:
        bpm = float(np.asarray(bpm, dtype=float).item())
    except Exception:
        print("❌ Your function should return one number: the heart rate in beats per minute.")
        return
    if not np.isfinite(bpm):
        print(f"❌ Your function gave {bpm}, which isn't a heart rate. Did it find any beats?")
        return

    print(f"Your function: {bpm:.1f} beats per minute")
    print(f"By hand:       {bpm_by_hand:.1f} beats per minute")

    if 60 <= bpm <= 100:
        print("✅ Plausible: it's in the 60 to 100 range of a resting heart.")
    else:
        print("❌ Not plausible for a resting heart (60 to 100).")

    if abs(bpm - bpm_by_hand) <= 8:
        print("✅ It matches your by-hand answer.")
    else:
        print("❌ It doesn't match your by-hand answer. Either the code or your counting is wrong. Which one?")


# ---------------- the simulated board ----------------
class SimulatedDAQ:
    """A pretend data-acquisition board.

    Data sheet
    ----------
    ADC resolution : 10 bit
    Input range    : 0 V to 5 V
    Channel 0      : ECG, after the amplifier (baseline sits at mid-range)
    Channel 1      : test tone from a function generator
    Channel 2      : precision reference, wired to a known, fixed voltage
    """
    BITS = 10
    VREF = 5.0
    V_OFFSET = 2.5

    def __init__(self, heart_rate=75, seed=None):
        self.heart_rate = heart_rate
        self._rng = np.random.default_rng(seed)

    # ---- the "analogue world": the voltage at any moment in time ----
    def _ecg(self, t):
        T = 60.0 / self.heart_rate
        tau = ((t - 0.4 + T / 2) % T) - T / 2          # time since the nearest R peak
        wave = lambda a, c, w: a * np.exp(-0.5 * ((tau - c) / w) ** 2)
        return (wave(0.15, -0.20, 0.025)      # P wave
                + wave(-0.12, -0.035, 0.010)  # Q
                + wave(1.00, 0.0, 0.012)      # R
                + wave(-0.25, 0.035, 0.012)   # S
                + wave(0.30, 0.25, 0.045))    # T wave

    def _analogue(self, channel, t, with_noise=True):
        if channel == 0:
            v = self.V_OFFSET + self._ecg(t)
            if with_noise:
                v = v + 0.08 * np.sin(2 * np.pi * 50 * t)        # 50 Hz mains hum
                v = v + self._rng.normal(0, 0.01, t.shape)       # electronic noise
        elif channel == 1:
            v = self.V_OFFSET + 1.0 * np.sin(2 * np.pi * 40 * t)          # 40 Hz test tone
            if with_noise:
                v = v + self._rng.normal(0, 0.003, t.shape)
        elif channel == 2:
            v = np.full(t.shape, 2.000)                          # exactly 2.000 V
            if with_noise:
                v = v + self._rng.normal(0, 0.001, t.shape)
        else:
            raise ValueError("This board only has channels 0, 1 and 2")
        return v

    # ---- what your code can call ----
    def read_adc(self, channel, n_samples, fs):
        """Return n_samples raw ADC counts (integers), sampled at fs Hz."""
        t = np.arange(n_samples) / fs
        v = self._analogue(channel, t)
        counts = np.floor(v / self.VREF * 2 ** self.BITS)
        return np.clip(counts, 0, 2 ** self.BITS - 1).astype(int)

# ---------------- Part 6: show the beats ----------------
def show_beats(t, signal, beats):
    """Plot the signal with a red dot on every beat your function found."""
    if beats is None:
        print("⏳ Your function doesn't give anything back yet. Does it `return` the beats?")
        return
    try:
        beats = np.asarray(beats, dtype=float)
    except Exception:
        print("❌ Your function should return the sample numbers of the beats, e.g. [100, 300].")
        return
    if beats.ndim != 1 or not np.all(beats == np.round(beats)):
        print("❌ Your function should return whole sample numbers (like 100 and 300), not times in seconds.")
        return
    beats = beats.astype(int)
    if len(beats) and (beats.min() < 0 or beats.max() >= len(signal)):
        print(f"❌ Some of your numbers are outside the recording (samples 0 to {len(signal) - 1}).")
        return
    plt.figure(figsize=(9, 3))
    plt.plot(t, signal)
    plt.plot(t[beats], signal[beats], "ro")
    plt.xlabel("time (s)")
    plt.ylabel("voltage (V)")
    plt.show()
    n = len(beats)
    where = ", at t = " + ", ".join(f"{x:.2f}" for x in t[beats]) + " s" if 0 < n <= 6 else ""
    print(f"Found {n} beats{where}.")
    if 2 <= n <= 3:
        print("✅ That's the 2 to 3 beats you predicted in Part 1. Is every dot on an R wave?")
    else:
        print("❌ You predicted 2 to 3 beats in 2 seconds in Part 1. Look at where the dots are.")

        

