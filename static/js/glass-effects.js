/**
 * ============================================================================
 * DocuDroid - 3D Glassmorphism Physics & Audio Micro-Interaction Engine
 * Hardware-accelerated 3D tilt, specular glare tracking, ambient particle
 * movement, and synthetic Web Audio micro-haptics.
 * ============================================================================
 */

(function () {
  'use strict';

  // State
  const state = {
    soundEnabled: localStorage.getItem('docudroid_sound') !== 'false',
    audioCtx: null,
  };

  /**
   * Web Audio Micro-Haptic Generator (Pure synthetic sound, zero asset loading)
   */
  function initAudioContext() {
    if (!state.audioCtx && typeof window.AudioContext !== 'undefined') {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      state.audioCtx = new AudioCtx();
    }
  }

  function playSound(type) {
    if (!state.soundEnabled) return;
    try {
      initAudioContext();
      if (!state.audioCtx) return;
      if (state.audioCtx.state === 'suspended') {
        state.audioCtx.resume();
      }

      const now = state.audioCtx.currentTime;
      const osc = state.audioCtx.createOscillator();
      const gain = state.audioCtx.createGain();

      osc.connect(gain);
      gain.connect(state.audioCtx.destination);

      if (type === 'click') {
        // Soft metallic glass tick
        osc.type = 'sine';
        osc.frequency.setValueAtTime(800, now);
        osc.frequency.exponentialRampToValueAtTime(400, now + 0.04);
        gain.gain.setValueAtTime(0.08, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);
        osc.start(now);
        osc.stop(now + 0.04);
      } else if (type === 'switch') {
        // Mode transition chime
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(520, now);
        osc.frequency.exponentialRampToValueAtTime(880, now + 0.08);
        gain.gain.setValueAtTime(0.06, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
        osc.start(now);
        osc.stop(now + 0.08);
      } else if (type === 'send') {
        // Upward energetic whoosh blip
        osc.type = 'sine';
        osc.frequency.setValueAtTime(320, now);
        osc.frequency.exponentialRampToValueAtTime(1040, now + 0.12);
        gain.gain.setValueAtTime(0.1, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
        osc.start(now);
        osc.stop(now + 0.12);
      } else if (type === 'receive') {
        // Warm glass droplet notification
        osc.type = 'sine';
        osc.frequency.setValueAtTime(660, now);
        osc.frequency.setValueAtTime(880, now + 0.06);
        gain.gain.setValueAtTime(0.08, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.16);
        osc.start(now);
        osc.stop(now + 0.16);
      } else if (type === 'success') {
        // Success chord
        const osc2 = state.audioCtx.createOscillator();
        const gain2 = state.audioCtx.createGain();
        osc2.connect(gain2);
        gain2.connect(state.audioCtx.destination);

        osc.type = 'sine';
        osc.frequency.setValueAtTime(523.25, now); // C5
        osc2.type = 'sine';
        osc2.frequency.setValueAtTime(659.25, now); // E5

        gain.gain.setValueAtTime(0.07, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.2);
        gain2.gain.setValueAtTime(0.07, now);
        gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.2);

        osc.start(now);
        osc2.start(now);
        osc.stop(now + 0.2);
        osc2.stop(now + 0.2);
      }
    } catch (e) {
      // Ignore audio failure quietly
    }
  }

  /**
   * 3D Tilt Card Physics Engine
   */
  function initTiltElements() {
    const cards = document.querySelectorAll('.tilt-card, [data-tilt]');

    cards.forEach((card) => {
      let bounds;

      function onMouseEnter() {
        bounds = card.getBoundingClientRect();
      }

      function onMouseMove(e) {
        if (!bounds) bounds = card.getBoundingClientRect();
        const mouseX = e.clientX - bounds.left;
        const mouseY = e.clientY - bounds.top;

        const xPct = (mouseX / bounds.width - 0.5) * 2;
        const yPct = (mouseY / bounds.height - 0.5) * 2;

        const maxAngle = parseFloat(card.dataset.tiltMax || '10');
        const rotX = -yPct * maxAngle;
        const rotY = xPct * maxAngle;

        card.style.setProperty('--rot-x', `${rotX.toFixed(2)}deg`);
        card.style.setProperty('--rot-y', `${rotY.toFixed(2)}deg`);
        card.style.setProperty('--scale', '1.02');
        card.style.setProperty('--mouse-x', `${mouseX}px`);
        card.style.setProperty('--mouse-y', `${mouseY}px`);
      }

      function onMouseLeave() {
        card.style.setProperty('--rot-x', '0deg');
        card.style.setProperty('--rot-y', '0deg');
        card.style.setProperty('--scale', '1');
      }

      card.addEventListener('mouseenter', onMouseEnter, { passive: true });
      card.addEventListener('mousemove', onMouseMove, { passive: true });
      card.addEventListener('mouseleave', onMouseLeave, { passive: true });
    });
  }

  /**
   * Ambient Mouse Glow Follower
   */
  function initMouseGlow() {
    const glow = document.querySelector('.mouse-glow');
    if (!glow) return;

    let targetX = window.innerWidth / 2;
    let targetY = window.innerHeight / 2;
    let currentX = targetX;
    let currentY = targetY;

    window.addEventListener(
      'mousemove',
      (e) => {
        targetX = e.clientX;
        targetY = e.clientY;
      },
      { passive: true }
    );

    function animateGlow() {
      // Smooth lerp (linear interpolation)
      currentX += (targetX - currentX) * 0.12;
      currentY += (targetY - currentY) * 0.12;

      glow.style.left = `${currentX}px`;
      glow.style.top = `${currentY}px`;

      requestAnimationFrame(animateGlow);
    }

    requestAnimationFrame(animateGlow);
  }

  /**
   * Toast Notification Controller
   */
  function showToast(message, type = 'info', duration = 3200) {
    let container = document.querySelector('.toast-container');
    if (!container) {
      container = document.createElement('div');
      container.className = 'toast-container';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `glass-toast toast-${type}`;

    let iconSvg = '';
    if (type === 'success') {
      iconSvg = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>';
      playSound('success');
    } else if (type === 'error') {
      iconSvg = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>';
    } else {
      iconSvg = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>';
    }

    toast.innerHTML = `${iconSvg}<span>${message}</span>`;
    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px) scale(0.95)';
      toast.style.transition = 'all 0.25s ease';
      setTimeout(() => toast.remove(), 250);
    }, duration);
  }

  /**
   * Modal Dialog Helper
   */
  function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) return;
    modal.classList.add('active');
    playSound('click');
  }

  function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (!modal) return;
    modal.classList.remove('active');
    playSound('click');
  }

  // Global Export
  window.DocuDroidFX = {
    playSound,
    showToast,
    openModal,
    closeModal,
    initTiltElements,
    toggleSound: function () {
      state.soundEnabled = !state.soundEnabled;
      localStorage.setItem('docudroid_sound', state.soundEnabled ? 'true' : 'false');
      showToast(state.soundEnabled ? 'Sound FX Enabled 🔊' : 'Sound FX Muted 🔇', 'info', 1800);
      return state.soundEnabled;
    },
    isSoundEnabled: function () {
      return state.soundEnabled;
    }
  };

  // Auto initialize on DOM ready
  document.addEventListener('DOMContentLoaded', () => {
    initMouseGlow();
    initTiltElements();

    // Attach click listeners for any element with data-sound
    document.addEventListener('click', (e) => {
      const btn = e.target.closest('[data-sound]');
      if (btn) {
        playSound(btn.dataset.sound || 'click');
      }
    });

    // Close modals on backdrop click or ESC
    document.addEventListener('click', (e) => {
      if (e.target.classList.contains('glass-modal-overlay')) {
        e.target.classList.remove('active');
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        document.querySelectorAll('.glass-modal-overlay.active').forEach((m) => {
          m.classList.remove('active');
        });
      }
    });
  });
})();
