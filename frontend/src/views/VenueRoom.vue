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
      <div v-if="me && (me.won || me.game_over) && !roundComplete" class="result" data-testid="result">
        <span v-if="me.won">You win!</span>
        <span v-else>Game over.</span>
      </div>
      <div v-if="roundComplete" class="ranking-section" data-testid="ranking-section">
        <h2 class="ranking-title">第 {{ currentRound }} 轮排名</h2>
        <table class="ranking-table">
          <thead>
            <tr>
              <th>名次</th>
              <th>用户名</th>
              <th>结果</th>
              <th>掷骰次数</th>
              <th>用时(秒)</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="r in ranking"
              :key="r.user_id"
              :class="{ me: r.user_id === myUserId }"
              data-testid="ranking-row"
            >
              <td>{{ r.rank }}</td>
              <td>{{ r.username }}</td>
              <td>{{ r.won ? '胜利' : '失败' }}</td>
              <td>{{ r.roll_count }}</td>
              <td>{{ r.duration_seconds.toFixed(1) }}</td>
            </tr>
          </tbody>
        </table>
        <button
          type="button"
          class="primary"
          data-testid="start-new-race"
          @click="onStartNewRace"
        >
          开始新比赛
        </button>
      </div>
      <button
        v-if="!roundComplete"
        class="primary"
        type="button"
        data-testid="roll"
        :disabled="!canRoll"
        @click="onRoll"
      >
        掷骰
      </button>
      <div class="history-section">
        <button
          type="button"
          class="secondary"
          data-testid="toggle-history"
          @click="showHistory = !showHistory"
        >
          {{ showHistory ? '收起' : '历史成绩' }}
        </button>
        <template v-if="showHistory">
          <ul v-if="rounds.length" class="rounds-list">
            <li
              v-for="r in rounds"
              :key="r.round_number"
              class="round-item"
            >
              <button
                type="button"
                class="round-btn"
                :class="{ active: selectedRound === r.round_number }"
                data-testid="round-link"
                @click="selectRound(r.round_number)"
              >
                第 {{ r.round_number }} 轮 ({{ formatRoundTime(r.started_at) }})
              </button>
            </li>
          </ul>
          <div v-if="selectedRound !== null && historyResults.length" class="history-ranking">
            <h3>第 {{ selectedRound }} 轮结果</h3>
            <table class="ranking-table">
              <thead>
                <tr>
                  <th>名次</th>
                  <th>用户名</th>
                  <th>结果</th>
                  <th>掷骰次数</th>
                  <th>用时(秒)</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="hr in historyResults"
                  :key="hr.user_id"
                  data-testid="history-ranking-row"
                >
                  <td>{{ hr.rank }}</td>
                  <td>{{ hr.username }}</td>
                  <td>{{ hr.won ? '胜利' : '失败' }}</td>
                  <td>{{ hr.roll_count }}</td>
                  <td>{{ hr.duration_seconds.toFixed(1) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <p v-else-if="rounds.length === 0" class="no-history">暂无历史轮次</p>
        </template>
      </div>
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
  { user_id: number; username: string; position: number; condition: number; mode: string; won: boolean; game_over: boolean; roll_count?: number }[]
>([]);
const currentRound = ref(1);
const roundComplete = ref(false);
const ranking = ref<
  { rank: number; user_id: number; username: string; won: boolean; game_over: boolean; roll_count: number; duration_seconds: number }[]
>([]);
const loadError = ref('');
const mode = ref<'normal' | 'super'>('normal');
const lastDice = ref<number | null>(null);
const lastSteps = ref<number | null>(null);
const myUserId = ref<number | null>(null);
const showHistory = ref(false);
const rounds = ref<{ round_number: number; started_at: string }[]>([]);
const selectedRound = ref<number | null>(null);
const historyResults = ref<
  { rank: number; user_id: number; username: string; won: boolean; game_over: boolean; roll_count: number; duration_seconds: number }[]
>([]);
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
  currentRound.value = data.current_round ?? 1;
  roundComplete.value = data.round_complete ?? false;
  ranking.value = data.ranking ?? [];
  const m = myUserId.value !== null ? data.participants.find((p: { user_id: number }) => p.user_id === myUserId.value) : null;
  if (m && !hadParticipants) mode.value = m.mode === 'super' ? 'super' : 'normal';
}

async function onStartNewRace() {
  const res = await apiFetch(`/venues/${venueId.value}/start_new_race`, { method: 'POST' });
  if (!res.ok) return;
  await loadVenue();
  rounds.value = [];
  selectedRound.value = null;
  historyResults.value = [];
}

function formatRoundTime(iso: string) {
  if (!iso) return '';
  try {
    const d = new Date(iso);
    return d.toLocaleString('zh-CN', { month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' });
  } catch {
    return iso.slice(0, 16);
  }
}

async function loadRounds() {
  const res = await apiFetch(`/venues/${venueId.value}/rounds`);
  if (!res.ok) return;
  rounds.value = await res.json();
}

async function selectRound(roundNumber: number) {
  selectedRound.value = roundNumber;
  const res = await apiFetch(`/venues/${venueId.value}/rounds/${roundNumber}/results`);
  if (!res.ok) {
    historyResults.value = [];
    return;
  }
  historyResults.value = await res.json();
}

watch(showHistory, (visible) => {
  if (visible && rounds.value.length === 0) loadRounds();
});

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
.ranking-section {
  margin-bottom: 16px;
}
.ranking-title {
  font-size: 18px;
  margin: 0 0 10px;
}
.ranking-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 12px;
  font-size: 14px;
}
.ranking-table th,
.ranking-table td {
  padding: 8px 10px;
  text-align: left;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}
.ranking-table th {
  font-weight: 700;
  color: rgba(0, 0, 0, 0.7);
}
.ranking-table tr.me {
  background: rgba(0, 102, 204, 0.08);
  font-weight: 600;
}
.secondary {
  padding: 8px 12px;
  border-radius: 10px;
  border: 1px solid rgba(0, 0, 0, 0.2);
  background: rgba(0, 0, 0, 0.04);
  cursor: pointer;
  font-weight: 600;
  margin-top: 16px;
}
.history-section {
  margin-top: 20px;
  padding-top: 16px;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
}
.rounds-list {
  list-style: none;
  padding: 0;
  margin: 10px 0 0;
}
.round-item {
  margin-bottom: 6px;
}
.round-btn {
  padding: 6px 10px;
  border-radius: 8px;
  border: 1px solid rgba(0, 0, 0, 0.15);
  background: #fff;
  cursor: pointer;
  font-size: 14px;
  width: 100%;
  text-align: left;
}
.round-btn.active {
  background: rgba(0, 102, 204, 0.12);
  border-color: rgba(0, 102, 204, 0.3);
}
.history-ranking {
  margin-top: 12px;
}
.history-ranking h3 {
  font-size: 16px;
  margin: 0 0 8px;
}
.no-history {
  margin: 10px 0 0;
  color: rgba(0, 0, 0, 0.5);
  font-size: 14px;
}
</style>
