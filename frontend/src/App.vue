<template>
  <main>
    <div class="container">
      <h1><span>adopt</span> a dog</h1>
      <SearchBox v-model:query="query" :disabled="loading" @search="handleQuerySubmit" />
      <Suggestions v-if="query.length === 0" @suggestion-click="handleSuggestionClick" />
      <div v-if="error !== null">{{ error }}</div>
      <DogCard v-for="dog in matchingDogs" :key="dog.id" :dog="dog" />
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import SearchBox from './components/SearchBox.vue'
import Suggestions from './components/Suggestions.vue'
import DogCard from './components/DogCard.vue'

const query = ref('')
const loading = ref(false)
const error = ref(null)
const matchingDogs = ref<DogResponse[]>([])

const handleSuggestionClick = (content: string) => {
  query.value = content
}

const handleQuerySubmit = async () => {
  loading.value = true
  try {
    const response = await fetch(`${import.meta.env.VITE_BACKEND_API_URL}/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: query.value }),
    })
    const json = await response.json()
    matchingDogs.value = json.results
  } catch (err) {
    console.log(err)
    error.value = err
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
main {
  background-color: var(--color-surface-0);
  width: 100vw;
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 1rem;
}

.container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 2.25rem;
  padding-block: 1rem;
  width: 90%;
}

@media (min-width: 640px) {
  .container {
    width: 70%;
  }
}

@media (min-width: 1024px) {
  .container {
    width: 45%;
  }
}

@media (min-width: 1200px) {
  .container {
    width: 40%;
  }
}

h1 {
  font-size: 3rem;
  font-weight: 600;
  text-align: center;
  user-select: none;
}

h1 span {
  color: var(--color-primary);
}
</style>
