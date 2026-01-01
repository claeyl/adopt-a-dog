<template>
  <div
    aria-label="Searchbox for describing your ideal dog"
    class="flex flex-col justify-between items-start gap-4 rounded-xl p-4 bg-surface-20 border-2 border-transparent transition-[border-color] duration-500"
    :class="{ focused: focused }"
  >
    <textarea
      ref="textareaRef"
      id="searchbox-input"
      class="w-full bg-transparent border-none text-inherit text-lg resize-none overflow-hidden disabled:opacity-50 placeholder:opacity-90 focus:outline-none"
      :minlength="MINIMUM_QUERY_LENGTH"
      :maxlength="MAXIMUM_QUERY_LENGTH"
      :value="query"
      placeholder="Describe your ideal dog..."
      :disabled="disabled"
      @input="handleInput"
      @focus="focused = true"
      @blur="focused = false"
      @keydown="handleKeyDown"
    >
    </textarea>
    <button
      aria-label="submit query"
      class="bg-primary border-none rounded-xl p-2 self-end aspect-square hover:brightness-85 disabled:opacity-50 disabled:cursor-not-allowed"
      :disabled="
        disabled ||
        query.trim().length < MINIMUM_QUERY_LENGTH ||
        query.trim().length > MAXIMUM_QUERY_LENGTH
      "
      @click="handleSearchClick"
    >
      <ArrowUp />
    </button>

    <p class="text-sm font-medium self-end text-surface-70 select-none">
      {{ `${query.length}/${MAXIMUM_QUERY_LENGTH}` }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import { ArrowUp } from 'lucide-vue-next'

const MINIMUM_QUERY_LENGTH = 3
const MAXIMUM_QUERY_LENGTH = 300
const ASCII_PRINTABLE_REGEX = /[^\x20-\x7E\n\r\t]/g

defineProps<{
  disabled: boolean
}>()

const emit = defineEmits<{
  (e: 'search'): void
}>()

const query = defineModel<string>('query', { required: true })
const textareaRef = ref<HTMLTextAreaElement | null>(null)
const focused = ref(false)

const adjustHeight = () => {
  if (textareaRef.value) {
    textareaRef.value.style.height = 'max-content'
    textareaRef.value.style.height = textareaRef.value.scrollHeight + 'px'
  }
}

watch(
  () => query.value,
  async () => {
    await nextTick()
    adjustHeight()
  },
)

const handleInput = (e: Event) => {
  const value = (e.target as HTMLTextAreaElement).value
  const sanitizedValue = value.replace(ASCII_PRINTABLE_REGEX, '')
  query.value = sanitizedValue
}

const handleKeyDown = (e: KeyboardEvent) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()

    validateSearchInput()
  }
}

const handleSearchClick = () => {
  validateSearchInput()
}

const validateSearchInput = () => {
  const trimmedQuery = query.value.trim()
  if (trimmedQuery.length >= MINIMUM_QUERY_LENGTH && trimmedQuery.length <= MAXIMUM_QUERY_LENGTH) {
    emit('search')
  }
}
</script>

<style scoped>
div.focused {
  border-color: var(--color-primary);
}
</style>
