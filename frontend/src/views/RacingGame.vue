<template>
  <div class="page">
    <header class="hero">
      <div>
        <h1 class="title">Racing Game</h1>
        <p class="subtitle">Roll the dice to advance your car.</p>
      </div>
    </header>

    <section class="panel">
      <div class="stats">
        <div class="stat">
          <div class="label">Position</div>
          <div class="value" data-testid="position">{{ state.position }}</div>
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

      <button
        class="primary"
        type="button"
        data-testid="roll"
        @click="onRoll"
      >
        Roll dice
      </button>
    </section>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue';
import type { GameState } from '../racing/engine';
import { createInitialState, roll } from '../racing/engine';

const props = defineProps<{
  diceRoller?: () => number;
}>();

const diceRoller = props.diceRoller ?? (() => Math.floor(Math.random() * 6) + 1);

const state = reactive<GameState>(createInitialState());
const lastDice = ref<number | null>(null);
const lastSteps = ref<number | null>(null);

const onRoll = () => {
  const dice = diceRoller();
  const result = roll(state, 'normal', dice);

  lastDice.value = dice;
  lastSteps.value = result.steps;
  state.position = result.newPosition;
  state.condition = result.newCondition;
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

.stats {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
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

.primary:active {
  transform: translateY(1px);
}
</style>
