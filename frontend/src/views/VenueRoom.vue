<template>
  <div class="page">
    <h1 class="title">{{ venueName }}</h1>
    <p v-if="loadError" class="error">{{ loadError }}</p>
    <template v-else>
      <div class="track" aria-label="Track">
        <div
          v-for="i in trackCells"
          :key="i"
          class="cell"
          :class="{ active: isCellActive(i) }"
          data-testid="track-cell"
        >
          <span class="cell-index">{{ i + 1 }}</span>
        </div>
        <template v-for="p in participants" :key="p.user_id">
          <div
            class="car"
            :class="{ me: p.user_id === myUserId }"
            :style="carStyle(p.position)"
            :data-pos="String(p.position)"
            :data-testid="'car-' + p.username"
          >
            <span class="username">{{ p.username }}</span>
            <span aria-hidden="true">🚗</span>
          </div>
        </template>
      </div>
      <div v-if="me" class="my-stats">
        <div class="stat">
          <span class="label">我的位置</span>
          <span data-testid="my-position">{{ me.position }}</span>
        </div>
        <div class="stat">
          <span class="label">车况</span>
          <span data-testid="my-condition">{{ me.condition }}</span>
        </div>
        <div class="stat">
          <span class="label">上次骰子</span>
          <span data-testid="my-dice">{{ lastDice ?? '—' }}</span>
        </div>
        <div class="stat">
          <span class="label">上次步数</span>
          <span data-testid="my-steps">{{ lastSteps ?? '—' }}</span>
        </div>
      </div>
      <div class="mode-row" role="group">
        <button
          class="seg"
          :class="{ active: mode === 'normal' }"
          type="button"
          :disabled="mode === 'super'"
          @click="mode = 'normal'"
        >
          Normal
        </button>
        <button
          class="seg"
          :class="{ active: mode === 'super' }"
          type="button"
          @click="mode = 'super'"
        >
          Super
        </button>
      </div>
      <div v-if="me && (me.won || me.game_over)" class="result" data-testid="result">
        <span v-if="me.won">You win!</span>
        <span v-else>Game over.</span>
      </div>
      <button
        class="primary"
        type="button"
        data-testid="roll"
        :disabled="!canRoll"
        @click="onRoll"
      >
        掷骰
      </button>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { apiFetch } from '../auth';
import { TRACK_LENGTH } from '../racing/engine';

const route = useRoute();
const venueId = computed(() => route.params.id as string);
const venueName = ref('');
const participants = ref<
  { user_id: number; username: string; position: number; condition: number; mode: string; won: boolean; game_over: boolean }[]
>([]);
const loadError = ref('');
const mode = ref<'normal' | 'super'>('normal');
const lastDice = ref<number | null>(null);
const lastSteps = ref<number | null>(null);
const myUserId = ref<number | null>(null);
let pollInterval: ReturnType<typeof setInterval> | null = null;

const trackCells = Array.from({ length: TRACK_LENGTH }, (_, i) => i);
const columns = 11;

function carStyle(position: number) {
  const row = Math.floor(position / columns) + 1;
  const col = (position % columns) + 1;
  return { gridRow: String(row), gridColumn: String(col) };
}

function isCellActive(_i: number) {
  return false;
}

const me = computed(() => {
  if (myUserId.value === null) return null;
  return participants.value.find((p) => p.user_id === myUserId.value) ?? null;
});

const canRoll = computed(() => {
  const m = me.value;
  return m && !m.won && !m.game_over;
});

async function loadMe() {
  const res = await apiFetch('/auth/me');
  if (!res.ok) return;
  const data = await res.json();
  myUserId.value = data.id;
}

async function loadVenue() {
  const res = await apiFetch(`/venues/${venueId.value}`);
  if (!res.ok) {
    loadError.value = '加载失败';
    return;
  }
  const data = await res.json();
  const hadParticipants = participants.value.length > 0;
  venueName.value = data.name;
  participants.value = data.participants;
  const m = myUserId.value !== null ? data.participants.find((p: { user_id: number }) => p.user_id === myUserId.value) : null;
  if (m && !hadParticipants) mode.value = m.mode === 'super' ? 'super' : 'normal';
}

onMounted(async () => {
  if (myUserId.value === null) await loadMe();
  await apiFetch(`/venues/${venueId.value}/enter`, { method: 'POST' }).then((r) => r.ok && r.json()).catch(() => null);
  await loadVenue();
  pollInterval = setInterval(loadVenue, 3000);
});

onUnmounted(() => {
  if (pollInterval) clearInterval(pollInterval);
});

watch(venueId, () => {
  loadVenue();
});

async function onRoll() {
  if (!canRoll.value) return;
  const res = await apiFetch(`/venues/${venueId.value}/roll`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ mode: mode.value }),
  });
  if (!res.ok) return;
  const data = await res.json();
  lastDice.value = data.dice;
  lastSteps.value = data.steps;
  await loadVenue();
}
</script>

<style scoped>
.page {
  max-width: 640px;
  margin: 0 auto;
}
.title {
  margin: 0 0 16px;
  font-size: 24px;
}
.error {
  color: #c00;
  margin: 0 0 12px;
}
.track {
  display: grid;
  grid-template-columns: repeat(11, 1fr);
  gap: 4px;
  margin-bottom: 16px;
  position: relative;
}
.cell {
  aspect-ratio: 1;
  border-radius: 8px;
  background: rgba(0, 0, 0, 0.06);
  display: grid;
  place-items: center;
}
.cell.active {
  background: rgba(0, 102, 204, 0.12);
}
.cell-index {
  font-size: 12px;
  color: rgba(0, 0, 0, 0.55);
}
.car {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 14px;
  transform: scaleX(-1);
}
.car.me {
  font-weight: 700;
  color: #0066cc;
}
.username {
  font-size: 10px;
  max-width: 48px;
  overflow: hidden;
  text-overflow: ellipsis;
}
.my-stats {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
}
.stat {
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.label {
  font-size: 12px;
  color: rgba(0, 0, 0, 0.6);
}
.mode-row {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}
.seg {
  padding: 8px 14px;
  border-radius: 10px;
  border: 1px solid rgba(0, 0, 0, 0.2);
  background: rgba(0, 0, 0, 0.04);
  cursor: pointer;
  font-weight: 600;
}
.seg.active {
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
}
.seg:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.result {
  margin-bottom: 12px;
  padding: 12px;
  border-radius: 14px;
  background: rgba(0, 0, 0, 0.03);
  font-weight: 700;
}
.primary {
  padding: 12px 14px;
  border: 0;
  border-radius: 14px;
  background: linear-gradient(135deg, #0066cc, #00a3ff);
  color: white;
  font-weight: 700;
  cursor: pointer;
  width: 100%;
}
.primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>
