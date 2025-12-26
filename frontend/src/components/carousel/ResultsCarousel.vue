<template>
  <div class="carousel" role="carousel">
    <div class="carousel__track">
      <div v-for="(dog, index) in dogs" :key="dog.id" v-show="index === currentIndex">
        <DogCard
          :dog="dog"
          :style="{
            backgroundImage: 'linear-gradient(hsla(15, 13%, 11%, 0.3), hsla(15, 13%, 11%, 0.3)',
            backgroundColor: colors[index % colors.length],
          }"
        />
      </div>
    </div>

    <div class="carousel__nav-dots">
      <button
        type="button"
        ariaLabel="previous"
        class="carousel__nav-btn"
        :disabled="currentIndex === 0"
        @click="onClickPrev"
      >
        <i class="pi pi-caret-left"></i>
      </button>

      <button
        v-for="(dog, idx) in dogs"
        :key="dog.id"
        :class="{ active: idx === currentIndex }"
        @click="currentIndex = idx"
        aria-label="Go to slide"
        class="carousel__dot"
      ></button>

      <button
        type="button"
        ariaLabel="next"
        class="carousel__nav-btn"
        :disabled="currentIndex === dogs.length - 1"
        @click="onClickNext"
      >
        <i class="pi pi-caret-right"></i>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { DogResponse } from '@/types/DogResponse'
import DogCard from '../DogCard.vue'
import { ref } from 'vue'

const props = defineProps<{
  dogs: DogResponse[]
}>()

const colors = [
  'var(--clr-orange)',
  'var(--clr-purple)',
  'var(--clr-green)',
  'var(--clr-pink)',
  'var(--clr-darkblue)',
]
const currentIndex = ref(0)

const onClickPrev = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
  }
}

const onClickNext = () => {
  if (currentIndex.value < props.dogs.length - 1) {
    currentIndex.value++
  }
}
</script>

<style scoped>
.carousel {
  position: relative;
}

.carousel__nav-btn {
  border: none;
  cursor: pointer;
  border-radius: var(--radius-circle);
  color: var(--clr-primary);
  background-color: transparent;
  font-size: calc(var(--font-base) * 1.25);
  outline: none;
}

.carousel__nav-btn:hover {
  filter: brightness(85%);
}

.carousel__nav-btn:disabled {
  filter: opacity(40%);
}

.carousel__nav-dots {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: var(--space-1);
  margin-top: var(--space-2);
}

.carousel__dot {
  width: 12px;
  height: 12px;
  border-radius: var(--radius-circle);
  border: none;
  background: var(--clr-light);
  filter: opacity(30%);
  cursor: pointer;
}

.carousel__dot.active {
  background-color: var(--clr-light);
  filter: opacity(100%);
}
</style>
