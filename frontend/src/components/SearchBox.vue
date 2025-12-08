<template>
  <div :class="{ focused: focused }">
    <textarea
      ref="textareaRef"
      :value="query"
      placeholder="What are you looking for?"
      :disabled="disabled"
      @input="handleInput"
      @focus="focused = true"
      @blur="focused = false"
      @keydown="handleKeyDown"
    >
    </textarea>
    <button
      aria-label="submit"
      :disabled="disabled || query.trim().length === 0"
      @click="handleSearchClick"
    >
      <i class="pi pi-arrow-up" style="color: white"></i>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import 'primeicons/primeicons.css'

const props = defineProps<{
  query: string
  disabled: boolean
}>()

const emit = defineEmits<{
  (e: 'update:query', value: string): void
  (e: 'search'): void
}>()

const textareaRef = ref<HTMLTextAreaElement | null>(null)
const focused = ref(false)

const adjustHeight = () => {
  if (textareaRef.value) {
    textareaRef.value.style.height = 'max-content'
    textareaRef.value.style.height = textareaRef.value.scrollHeight + 'px'
  }
}

// It's like a useEffect
watch(
  () => props.query,
  async () => {
    await nextTick()
    adjustHeight()
  },
)

const handleInput = (e: Event) => {
  const value = (e.target as HTMLTextAreaElement).value
  emit('update:query', value)
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
  const trimmedQuery = props.query.trim()
  if (trimmedQuery.length > 0) {
    emit('search')
  }
}
</script>

<style scoped>
div {
  display: flex;
  flex-direction: column;
  align-items: start;
  justify-content: space-between;
  gap: 0.5rem;
  background-color: var(--color-surface-100);
  width: 100%;

  border-radius: 1rem;
  padding: 1.25rem;
  border: 1px solid transparent;

  transition: border-color 0.5s ease;
}

div.focused {
  border-color: var(--color-primary);
  border-width: 2px;
}

textarea {
  width: 100%;
  font-size: 1.25rem;
  background-color: transparent;
  border: none;
  color: inherit;
  font-family: sans-serif;
  resize: none;
  overflow: hidden;
}

textarea:disabled {
  color: hsla(0, 0%, 100%, 0.5);
}

textarea::placeholder {
  color: hsla(0, 0%, 100%, 0.5);
}

textarea:focus {
  outline: none;
}

button {
  background-color: var(--color-primary);
  border: none;
  border-radius: 0.5rem;
  padding: 0.5rem;
  align-self: flex-end;
  cursor: pointer;
}

button:hover {
  background-color: var(--color-primary-dark);
}

button:disabled {
  background-color: var(--color-surface-200);
}
</style>
