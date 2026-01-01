<script setup lang="ts">
import type { HttpError } from '@/types/Error'
import { CircleQuestionMark, SearchX, ServerCrash } from 'lucide-vue-next'

const props = defineProps<{
  error: HttpError
}>()

const errorMapping = (error: HttpError) => {
  switch (error) {
    case 'BadRequest':
      return {
        icon: CircleQuestionMark,
        title: "That doesn't seem right",
        description:
          "Your query doesn't seem to describe a dog. Try entering characteristics like size, temperament and lifestyle fit.",
      }
    case 'NotFound':
      return {
        icon: SearchX,
        title: 'No matches found',
        description:
          "We couldn't find dogs matching your search. Try broadening your search preferences.",
      }
    case 'InternalServerError':
      return {
        icon: ServerCrash,
        title: 'Server error',
        description:
          'Something went wrong on our end. Please try again in a moment. If the problem persists, please contact support.',
      }
  }
}

const errorComponents = errorMapping(props.error)
</script>

<template>
  <div class="flex flex-col items-center text-center gap-4">
    <div class="grid place-items-center w-20 aspect-square bg-danger/20 rounded-xl">
      <component
        :is="errorComponents.icon"
        color="var(--color-danger)"
        :size="54"
        :stroke-width="1.75"
      />
    </div>
    <h2 class="text-2xl font-semibold">{{ errorComponents.title }}</h2>
    <p class="text-balance text-surface-60 text-base/7">{{ errorComponents.description }}</p>
  </div>
</template>
