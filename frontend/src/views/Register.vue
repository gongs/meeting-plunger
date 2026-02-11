<template>
  <div class="page">
    <h1 class="title">注册</h1>
    <form class="form" @submit.prevent="onSubmit">
      <div class="field">
        <label for="username">用户名</label>
        <input
          id="username"
          v-model="username"
          type="text"
          required
          autocomplete="username"
          data-testid="register-username"
        />
      </div>
      <div class="field">
        <label for="password">密码</label>
        <input
          id="password"
          v-model="password"
          type="password"
          required
          autocomplete="new-password"
          data-testid="register-password"
        />
      </div>
      <p v-if="error" class="error" role="alert" data-testid="register-error">{{ error }}</p>
      <button type="submit" class="primary" :disabled="loading" data-testid="register-submit">
        {{ loading ? '注册中…' : '注册' }}
      </button>
    </form>
    <p class="foot">
      <RouterLink to="/login" data-testid="register-to-login">已有账号？去登录</RouterLink>
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { setToken } from '../auth';

const router = useRouter();
const username = ref('');
const password = ref('');
const error = ref('');
const loading = ref(false);

async function onSubmit() {
  error.value = '';
  loading.value = true;
  try {
    const res = await fetch('/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: username.value, password: password.value }),
    });
    const data = await res.json().catch(() => ({})) as { detail?: string };
    if (!res.ok) {
      error.value = data.detail ?? '注册失败';
      return;
    }
    setToken(data.token);
    await router.push('/venues');
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.page {
  max-width: 360px;
  margin: 0 auto;
}
.title {
  margin: 0 0 20px;
  font-size: 24px;
}
.form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.field label {
  font-weight: 600;
  font-size: 14px;
}
.field input {
  padding: 10px 12px;
  border: 1px solid rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  font-size: 16px;
}
.error {
  color: #c00;
  font-size: 14px;
  margin: 0;
}
.primary {
  padding: 12px 14px;
  border: 0;
  border-radius: 14px;
  background: linear-gradient(135deg, #0066cc, #00a3ff);
  color: white;
  font-weight: 700;
  cursor: pointer;
}
.primary:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
.foot {
  margin: 18px 0 0;
  font-size: 14px;
}
.foot a {
  color: #0066cc;
  text-decoration: none;
}
.foot a:hover {
  text-decoration: underline;
}
</style>
