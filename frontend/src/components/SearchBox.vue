<template>
  <div :class="{ focused: focused }" role="searchbox">
    <textarea
      ref="textareaRef"
      aria-label="searchbox-input"
      :maxlength="MAXIMUM_QUERY_LENGTH"
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
      :disabled="
        disabled ||
        query.trim().length < MINIMUM_QUERY_LENGTH ||
        query.trim().length > MAXIMUM_QUERY_LENGTH
      "
      @click="handleSearchClick"
    >
      <i class="pi pi-arrow-up"></i>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import 'primeicons/primeicons.css'

const MINIMUM_QUERY_LENGTH = 3
const MAXIMUM_QUERY_LENGTH = 1000
const ASCII_PRINTABLE_REGEX = /[^\x20-\x7E\n\r\t]/g

const props = defineProps<{
  disabled: boolean
}>()

const emit = defineEmits<{
  (e: 'search'): void
}>()

const query = defineModel<string>('query', { required: true })
const error = defineModel<string>('error', { required: true })

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
  error.value = ''
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
  } else if (trimmedQuery.length < MINIMUM_QUERY_LENGTH) {
    error.value = 'A few more words will help us find the best match for you.'
  }
}
</script>

<style scoped>
div {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: start;
  gap: var(--space-2);

  border-radius: var(--radius-lg);
  padding: var(--space-2);

  background-color: var(--clr-darkgrey);
  border: 2px solid transparent;

  transition: border-color 0.5s ease;
}

div.focused {
  border-color: var(--clr-primary);
}

textarea {
  width: 100%;
  background-color: transparent;
  border: none;
  color: inherit;
  font-size: var(--font-p-lg);
  resize: none;
  overflow: hidden;
}

textarea:disabled,
textarea::placeholder {
  filter: opacity(40%);
}

textarea:focus {
  outline: none;
}

button {
  background-color: var(--clr-primary);
  border: none;
  border-radius: var(--radius-lg);
  padding: var(--space-1);
  align-self: flex-end;
  cursor: pointer;
  color: var(--clr-darkgrey);
  aspect-ratio: 1 / 1;
}

button:hover {
  background-color: var(--clr-primary);
  filter: brightness(85%);
}

button:disabled {
  filter: opacity(40%);
}

button > i {
  font-weight: 800;
}
</style>
