<script setup lang="ts">
import Header from '@/components/Header.vue'
import SearchResultsDisplay from '@/components/SearchResultsDisplay.vue'
import Suggestions from '@/components/Suggestions.vue'
import SearchBox from '@/components/SearchBox.vue'
import { findDogs } from '@/api/findDogs'
import type { DogInfoResponse } from '@/types/DogInfoResponse'
import type { HttpError } from '@/types/Error'
import { onMounted, ref } from 'vue'

const dogs = ref<DogInfoResponse[]>([])
const loading = ref(false)
const error = ref<HttpError | undefined>(undefined)
const currentQuery = ref('')
const previousQuery = ref('')
const hasSearched = ref(false)

onMounted(() => {
  const savedDogsUnprocessed = sessionStorage.getItem('dogs')
  if (savedDogsUnprocessed) {
    const savedDogs = JSON.parse(savedDogsUnprocessed) as DogInfoResponse[]
    dogs.value = savedDogs
  }

  const savedQuery = sessionStorage.getItem('query')
  if (savedQuery) {
    previousQuery.value = savedQuery
  }
})

const handleSearch = async () => {
  const currentQueryValue = currentQuery.value

  loading.value = true
  hasSearched.value = true
  dogs.value = []
  error.value = undefined
  previousQuery.value = currentQuery.value
  currentQuery.value = ''

  try {
    dogs.value = await findDogs(currentQueryValue)
    sessionStorage.setItem('dogs', JSON.stringify(dogs.value))
    sessionStorage.setItem('query', currentQuery.value)
  } catch (err) {
    error.value = (err as HttpError) || 'InternalServerError'
  } finally {
    loading.value = false
  }
}

const reset = () => {
  dogs.value = []
  loading.value = false
  error.value = undefined
  currentQuery.value = ''
  previousQuery.value = ''
  hasSearched.value = false
  sessionStorage.clear()
}

const handleSuggestionClick = (content: string) => {
  currentQuery.value = content
}
</script>
<template>
  <div class="min-h-screen w-screen grid place-items-center">
    <Header @new-search="reset"></Header>

    <main class="flex flex-col gap-6 sm:w-[70%] lg:w-[45%] xl:w-[40%] w-[90%] mt-15 py-8">
      <div class="text-center" v-if="dogs.length === 0">
        <h1 class="text-5xl font-bold mb-5 select-none">
          <span class="text-primary">adopt</span> a dog
        </h1>
        <p class="text-surface-70 text-balance select-none">
          Searching for your best friend(s)? This site uses semantic search and reranking to find
          dogs matching your requirements from the Shenton Park Dogs' Refuge Home.
        </p>
      </div>

      <SearchBox v-model:query="currentQuery" :disabled="loading" @search="handleSearch" />
      <Suggestions v-if="dogs.length === 0" @suggestion-click="handleSuggestionClick" />
      <SearchResultsDisplay :dogs="dogs" :loading="loading" :error="error" :query="previousQuery" />
    </main>
  </div>
</template>
<style scoped></style>
