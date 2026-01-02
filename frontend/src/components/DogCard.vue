<script setup lang="ts">
import { Calendar, CircleDollarSign, DogIcon, Ruler, Sparkles, Weight } from 'lucide-vue-next'
import type { DogInfoResponse } from '@/types/DogInfoResponse'
import TypewriterText from './ui/TypewriterText.vue'

const props = defineProps<{
  index: number
  dog: DogInfoResponse
}>()

const formatAge = (age: number) => {
  if (age < 1) return '< 1 Year'
  if (age === 1) return '1 Year'
  return `${age} Years`
}

const dogStats = [
  {
    icon: Calendar,
    value: formatAge(props.dog.age),
  },
  {
    icon: Weight,
    value: props.dog.weight === 0 ? 'N/A' : `${props.dog.weight}kg`,
  },
  {
    icon: Ruler,
    value: props.dog.size,
  },
  {
    icon: CircleDollarSign,
    value: `AUD ${props.dog.adoptionFee}`,
  },
]
</script>
<template>
  <div
    class="bg-surface-10 border border-surface-20 rounded-xl transition-all duration-300 overflow-hidden animate-fade-in-up card"
    :style="{ animationDelay: `${index * 100}ms` }"
  >
    <!-- Header -->
    <header class="border-b border-surface-30 flex justify-between items-center p-6 gap-4">
      <div class="flex gap-4 items-center">
        <div
          class="grid place-items-center bg-green w-16 h-16 sm:w-20 sm:h-20 aspect-square rounded-xl"
        >
          <DogIcon :size="40" :stroke-width="1.75" />
          <!-- <img
            class="aspect-square max-w-full rounded-xl object-cover"
            src="https://www.dogshome.org.au/wp-content/uploads/2025/12/53d4874356c947278eac1151982e839a-1766294517-1766300321-jpg.jpg"
            alt="dog photo"
          /> -->
        </div>
        <div>
          <h3 class="font-semibold text-2xl sm:mb-2">
            <TypewriterText :content="dog.name"></TypewriterText>
          </h3>
          <p class="text-surface-60 capitalize text-balance">{{ dog.breed }}</p>
        </div>
      </div>
      <div
        class="border-2 rounded-full px-4 py-1 font-bold capitalize"
        :class="`${dog.gender === 'female' ? 'border-pink bg-pink/20 text-pink' : 'border-darkblue bg-darkblue/20 text-darkblue'}`"
      >
        {{ dog.gender }}
      </div>
    </header>

    <!-- Body -->
    <div class="flex flex-col p-6 gap-6">
      <!-- Stats -->
      <div class="grid grid-cols-2 gap-1 sm:grid-cols-4 place-items-stretch">
        <div class="flex items-center gap-2" v-for="(stat, index) in dogStats" :key="index">
          <component color="var(--color-surface-50)" :is="stat.icon" :size="20" />
          <span class="capitalize">{{ stat.value }}</span>
        </div>
      </div>

      <!-- Tags -->
      <div class="flex flex-wrap gap-2">
        <div
          class="py-1 px-4 rounded-full bg-surface-30 text-sm"
          v-for="(tag, index) in dog.tags"
          :key="index"
        >
          {{ tag }}
        </div>
      </div>

      <!-- Description -->
      <p class="opacity-75 text-base/7">{{ dog.description }}</p>

      <!-- Generated Explanation -->
      <div class="border border-primary/12 p-4 rounded-xl bg-primary/13">
        <strong class="flex items-center gap-2 mb-4"
          ><Sparkles color="var(--color-primary)" /><span
            >Why {{ dog.name }} might be perfect for you</span
          ></strong
        >
        <p class="text-base/7">{{ dog.explanation }}</p>
      </div>

      <!-- CTA -->
      <a
        class="w-full bg-primary text-center rounded-xl py-2 cursor-pointer font-semibold text-dark transition-brightness"
        :href="`https://www.dogshome.org.au/our-dogs/${dog.id}`"
        target="_blank"
        >Meet {{ dog.name }}</a
      >
    </div>
  </div>
</template>
<style scoped>
.card {
  box-shadow: 0 8px 30px -8px hsla(0, 0%, 0%, 0.4);
}

.card:hover {
  box-shadow: 0 12px 40px 5px hsla(0, 0%, 0%, 0.5);
}

@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fade-in-up 0.5s ease-out forwards;
}
</style>
