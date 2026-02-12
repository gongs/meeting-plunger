<template>
  <div class="page">
    <header class="hero">
      <div>
        <h1 class="title">Racing Game</h1>
        <p class="subtitle">
          Normal: odd → 1, even → 2 steps; no condition loss. Super: steps =
          min(dice, condition), 1 condition loss per roll; once Super, you
          cannot switch back.
        </p>
      </div>
    </header>

    <section class="panel">
      <div class="mode-row" role="group" aria-label="Mode">
        <button
          class="seg"
          :class="{ active: mode === 'normal' }"
          type="button"
          data-testid="mode-normal"
          :disabled="mode === 'super'"
          :aria-disabled="mode === 'super'"
          @click="mode = 'normal'"
        >
          Normal
        </button>
        <button
          class="seg"
          :class="{ active: mode === 'super' }"
          type="button"
          data-testid="mode-super"
          @click="mode = 'super'"
        >
          Super
        </button>
      </div>

      <div class="stats">
        <div class="stat">
          <div class="label">Position</div>
          <div class="value" data-testid="position">{{ state.position }}</div>
        </div>
        <div class="stat">
          <div class="label">Condition</div>
          <div class="value" data-testid="condition">{{ state.condition }}</div>
          <div class="condition-bar" aria-hidden="true">
            <span
              v-for="i in 6"
              :key="i"
              class="pip"
              :class="{ on: i <= state.condition }"
            />
          </div>
        </div>
        <div class="stat">
          <div class="label">Last dice</div>
          <div class="value" data-testid="dice">
            {{ lastDice === null ? '—' : lastDice }}
          </div>
        </div>
        <div class="stat">
          <div class="label">Last steps</div>
          <div class="value" data-testid="steps">
            {{ lastSteps === null ? '—' : lastSteps }}
          </div>
        </div>
      </div>

      <div class="hint" data-testid="damage" aria-live="polite">
        {{ lastDamage === null ? '—' : `Damage +${lastDamage}` }}
      </div>

      <div class="track-wrap racing-track-wrap">
        <div class="racing-track-curb" aria-hidden="true" />
        <div class="track racing-track" aria-label="Track">
          <div class="racing-track-center-line" aria-hidden="true" />
          <div
            v-for="i in trackCells"
            :key="i"
            class="cell racing-cell"
            :class="{
              'racing-cell--active': i === carPos,
              'racing-cell--start': i === 0,
              'racing-cell--finish': i === trackCells.length - 1,
            }"
            :aria-label="
              i === 0 ? 'Start' : i === trackCells.length - 1 ? 'Finish' : undefined
            "
            data-testid="track-cell"
          >
            <span v-if="i === 0" class="racing-cell-label">START</span>
            <span v-else-if="i === trackCells.length - 1" class="racing-cell-label">FINISH</span>
            <span class="racing-cell-index">{{ i + 1 }}</span>
          </div>
          <div
            class="car"
            data-testid="car"
            :data-pos="String(carPos)"
            :style="carStyle"
            aria-label="Your car"
            :class="{ damaged: lastDamage !== null && lastDamage > 0 }"
          >
            <span class="racing-car-icon" aria-hidden="true" />
          </div>
        </div>
        <div class="racing-track-curb" aria-hidden="true" />
      </div>

      <div
        v-if="status !== 'playing'"
        class="result"
        data-testid="result"
        aria-live="polite"
      >
        <span v-if="status === 'won'">You win!</span>
        <span v-else>Game over.</span>
      </div>

      <div class="actions">
        <button
          class="primary"
          type="button"
          data-testid="roll"
          :disabled="status !== 'playing'"
          @click="onRoll"
        >
          Roll dice
        </button>
        <button
          class="secondary"
          type="button"
          data-testid="restart"
          @click="onRestart"
        >
          Restart
        </button>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from 'vue';
import type { GameState } from '../racing/engine';
import type { Mode } from '../racing/engine';
import { createInitialState, roll, TRACK_LENGTH } from '../racing/engine';

const props = defineProps<{
  diceRoller?: () => number;
  initialState?: GameState;
}>();

const diceRoller = props.diceRoller ?? (() => Math.floor(Math.random() * 6) + 1);

const state = reactive<GameState>({ ...(props.initialState ?? createInitialState()) });
const mode = ref<Mode>('normal');
const lastDice = ref<number | null>(null);
const lastSteps = ref<number | null>(null);
const lastDamage = ref<number | null>(null);
const status = ref<'playing' | 'won' | 'gameOver'>('playing');
const carPos = computed(() =>
  Math.max(0, Math.min(TRACK_LENGTH - 1, state.position))
);
const trackCells = computed(() =>
  Array.from({ length: TRACK_LENGTH }, (_, i) => i)
);
const carStyle = computed(() => {
  return { gridRow: '1', gridColumn: String(carPos.value + 1) };
});

const onRoll = () => {
  if (status.value !== 'playing') return;

  const dice = diceRoller();
  const beforeCondition = state.condition;
  const result = roll(state, mode.value, dice);

  lastDice.value = dice;
  lastSteps.value = result.steps;
  state.position = result.newPosition;
  state.condition = result.newCondition;
  lastDamage.value =
    mode.value === 'super' && result.newCondition < beforeCondition ? 1 : null;

  if (result.won) status.value = 'won';
  else if (result.gameOver) status.value = 'gameOver';
};

const onRestart = () => {
  const next = createInitialState();
  state.position = next.position;
  state.condition = next.condition;

  mode.value = 'normal';
  status.value = 'playing';
  lastDice.value = null;
  lastSteps.value = null;
  lastDamage.value = null;
};
</script>

<style scoped>
.hero {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 18px;
  margin-bottom: 16px;
}

.title {
  margin: 0;
  font-size: 28px;
  letter-spacing: -0.2px;
}

.subtitle {
  margin: 6px 0 0;
  color: rgba(0, 0, 0, 0.7);
  max-width: 68ch;
}

.panel {
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.9);
  padding: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.06);
}

.mode-row {
  display: inline-flex;
  padding: 4px;
  border-radius: 14px;
  background: rgba(0, 0, 0, 0.04);
  border: 1px solid rgba(0, 0, 0, 0.08);
  margin-bottom: 12px;
}

.seg {
  padding: 10px 12px;
  border: 0;
  border-radius: 12px;
  background: transparent;
  font-weight: 800;
  cursor: pointer;
  color: rgba(0, 0, 0, 0.75);
}

.seg.active {
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
  color: rgba(0, 0, 0, 0.95);
}

.seg:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.stats {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 14px;
}

.stat {
  padding: 12px;
  border-radius: 14px;
  background: rgba(0, 102, 204, 0.06);
  border: 1px solid rgba(0, 102, 204, 0.1);
}

.label {
  font-size: 12px;
  color: rgba(0, 0, 0, 0.7);
  margin-bottom: 6px;
}

.value {
  font-weight: 800;
  font-size: 22px;
  letter-spacing: -0.2px;
}

.condition-bar {
  display: flex;
  gap: 6px;
  margin-top: 10px;
}

.pip {
  height: 8px;
  flex: 1 1 0;
  border-radius: 999px;
  background: rgba(0, 0, 0, 0.1);
}

.pip.on {
  background: rgba(0, 102, 204, 0.55);
}

.hint {
  margin: 4px 0 14px;
  font-size: 13px;
  color: rgba(0, 0, 0, 0.7);
}

.track-wrap {
  margin-bottom: 14px;
}

.car {
  display: grid;
  place-items: center;
  line-height: 1;
  pointer-events: none;
  transform: scaleX(-1);
}

.car.damaged {
  animation: shake 250ms ease-in-out;
}

.seg:focus-visible,
.primary:focus-visible,
.secondary:focus-visible {
  outline: 3px solid rgba(0, 102, 204, 0.35);
  outline-offset: 2px;
}

.result {
  margin: 0 0 14px;
  padding: 12px 12px;
  border-radius: 14px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: rgba(0, 0, 0, 0.03);
  font-weight: 900;
}

.actions {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 10px;
}

.primary {
  width: 100%;
  padding: 12px 14px;
  border: 0;
  border-radius: 14px;
  background: linear-gradient(135deg, #0066cc, #00a3ff);
  color: white;
  font-weight: 800;
  cursor: pointer;
  font-size: 16px;
}

.primary:hover {
  filter: brightness(0.98);
}

.primary:disabled {
  cursor: not-allowed;
  background: rgba(0, 0, 0, 0.22);
}

.primary:active {
  transform: translateY(1px);
}

.secondary {
  padding: 12px 14px;
  border-radius: 14px;
  background: rgba(0, 0, 0, 0.04);
  border: 1px solid rgba(0, 0, 0, 0.12);
  font-weight: 800;
  cursor: pointer;
}

.secondary:hover {
  background: rgba(0, 0, 0, 0.06);
}

@keyframes shake {
  0% {
    transform: scaleX(-1) translateX(0);
  }
  25% {
    transform: scaleX(-1) translateX(-2px);
  }
  50% {
    transform: scaleX(-1) translateX(2px);
  }
  75% {
    transform: scaleX(-1) translateX(-1px);
  }
  100% {
    transform: scaleX(-1) translateX(0);
  }
}
</style>
