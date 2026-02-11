<template>
  <div class="page">
    <header class="hero">
      <div>
        <h1 class="title">Racing Game</h1>
        <p class="subtitle">Roll the dice to advance your car.</p>
      </div>
    </header>

    <section class="panel">
      <div class="mode-row" role="group" aria-label="Mode">
        <button
          class="seg"
          :class="{ active: mode === 'normal' }"
          type="button"
          data-testid="mode-normal"
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

      <div class="hint" data-testid="damage">
        {{ lastDamage === null ? '—' : `Damage +${lastDamage}` }}
      </div>

      <div class="track" aria-label="Track">
        <div
          v-for="i in trackCells"
          :key="i"
          class="cell"
          :class="{ active: i === carPos }"
          data-testid="track-cell"
        >
          <span class="cell-index">{{ i + 1 }}</span>
        </div>

        <div
          class="car"
          data-testid="car"
          :data-pos="String(carPos)"
          :style="carStyle"
          aria-hidden="true"
        >
          🚗
        </div>
      </div>

      <div v-if="status !== 'playing'" class="result" data-testid="result">
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
  const columns = 11;
  const row = Math.floor(carPos.value / columns) + 1;
  const col = (carPos.value % columns) + 1;
  return { gridRow: String(row), gridColumn: String(col) };
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
  lastDamage.value = Math.max(0, beforeCondition - result.newCondition);

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

.hint {
  margin: 4px 0 14px;
  font-size: 13px;
  color: rgba(0, 0, 0, 0.7);
}

.track {
  position: relative;
  display: grid;
  grid-template-columns: repeat(11, minmax(0, 1fr));
  gap: 8px;
  margin-bottom: 14px;
}

.cell {
  aspect-ratio: 1 / 1;
  border-radius: 14px;
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: rgba(0, 0, 0, 0.02);
  display: flex;
  align-items: center;
  justify-content: center;
}

.cell.active {
  border-color: rgba(0, 102, 204, 0.5);
  background: rgba(0, 102, 204, 0.12);
}

.cell-index {
  font-size: 12px;
  color: rgba(0, 0, 0, 0.55);
  font-weight: 700;
}

.car {
  display: grid;
  place-items: center;
  font-size: 20px;
  line-height: 1;
  pointer-events: none;
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
</style>
