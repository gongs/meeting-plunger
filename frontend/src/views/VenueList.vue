<template>
  <div class="page">
    <h1 class="title">赛场列表</h1>
    <p v-if="error" class="error">{{ error }}</p>
    <ul v-else class="list">
      <li v-for="v in venues" :key="v.id" class="item">
        <span class="name">{{ v.name }}</span>
        <button type="button" class="btn" @click="enter(v.id)" data-testid="enter-venue">进入</button>
      </li>
    </ul>
    <form class="create" @submit.prevent="onCreate">
      <input v-model="newName" type="text" placeholder="新赛场名称" data-testid="new-venue-name" />
      <button type="submit" class="btn" data-testid="create-venue">创建赛场</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { apiFetch } from '../auth';

const router = useRouter();
const venues = ref<{ id: number; name: string }[]>([]);
const error = ref('');
const newName = ref('');

async function load() {
  const res = await apiFetch('/venues');
  if (!res.ok) {
    error.value = '加载失败';
    return;
  }
  venues.value = await res.json();
}

onMounted(load);

function enter(id: number) {
  router.push({ name: 'venue', params: { id: String(id) } });
}

async function onCreate() {
  if (!newName.value.trim()) return;
  const res = await apiFetch('/venues', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name: newName.value.trim() }),
  });
  if (!res.ok) {
    error.value = '创建失败';
    return;
  }
  newName.value = '';
  await load();
}
</script>

<style scoped>
.page {
  max-width: 480px;
  margin: 0 auto;
}
.title {
  margin: 0 0 20px;
  font-size: 24px;
}
.error {
  color: #c00;
  margin: 0 0 12px;
}
.list {
  list-style: none;
  padding: 0;
  margin: 0 0 24px;
}
.item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
}
.name {
  font-weight: 600;
}
.btn {
  padding: 8px 14px;
  border-radius: 10px;
  border: 1px solid rgba(0, 0, 0, 0.2);
  background: #fff;
  cursor: pointer;
  font-weight: 600;
}
.create {
  display: flex;
  gap: 10px;
  align-items: center;
}
.create input {
  flex: 1;
  padding: 10px 12px;
  border: 1px solid rgba(0, 0, 0, 0.2);
  border-radius: 10px;
}
</style>
