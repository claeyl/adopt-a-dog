<template>
  <main>
    <div class="title" v-if="matchingDogs.length === 0">
      <h1><span>adopt</span> a dog</h1>
      <p>
        Searching for your best friend(s)? Start describing your ideal dog. This site uses semantic
        search to find dogs matching your requirements from the Shenton Park Dogs' Refuge Home.
      </p>
    </div>
    <div v-else class="results">
      <p class="results__summary">
        Here are the dogs matching your query: {{ matchingDogsSummary }}
      </p>
      <DogCard v-for="dog in matchingDogs" :key="dog.id" :dog="dog" />
    </div>
    <div class="search">
      <SearchBox
        v-model:query="query"
        v-model:error="error"
        :disabled="loading"
        @search="handleQuerySubmit"
      />
      <!-- <Suggestions v-if="matching !== null" @suggestion-click="handleSuggestionClick" /> -->
      <div class="search__error" v-if="error !== null">{{ error }}</div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import SearchBox from './components/SearchBox.vue'
import Suggestions from './components/Suggestions.vue'
import DogCard from './components/DogCard.vue'

import data from './fake/fake_results.json'

const query = ref('')
const loading = ref(false)
const error = ref(null)

const matchingDogsSummary = ref('')
const matchingDogs = ref<DogResponse[]>([])

const handleSuggestionClick = (content: string) => {
  query.value = content
}

const handleQuerySubmit = async () => {
  loading.value = true
  matchingDogsSummary.value = query.value
  try {
    const response = await fetch(`${import.meta.env.VITE_BACKEND_API_URL}/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: query.value }),
    })
    const json = await response.json()
    matchingDogs.value = json.results
    // matchingDogs.value = data.results // for testing
  } catch (err) {
    console.log(err)
    error.value = err
  } finally {
    query.value = ''
    loading.value = false
  }
}
</script>

<style scoped>
main {
  display: flex;
  flex-direction: column;
  gap: 3rem;
  width: 90%;
}

@media (min-width: 640px) {
  main {
    width: 70%;
  }
}

@media (min-width: 1024px) {
  main {
    width: 45%;
  }
}

@media (min-width: 1200px) {
  main {
    width: 40%;
  }
}

.title {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  text-align: center;
}

.title h1 {
  font-size: 3rem;
  font-weight: 600;
  user-select: none;
}

.title h1 span {
  color: var(--color-primary);
}

.title p {
  text-wrap: balance;
  font-size: 1.1rem;
  color: hsla(0, 0%, 100%, 0.8);
}

.results__summary {
  width: 100%;
  text-align: center;
  border: solid 1px var(--color-surface-200);
  border-radius: 1rem;
  padding: 1rem;
  background-color: hsla(197, 100%, 31%, 30%);

  margin-bottom: 1rem;
}

.search {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.search__error {
  color: var(--color-error);
}
</style>
