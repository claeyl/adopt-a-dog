<template>
  <section class="card">
    <div class="card__header">
      <h2><TypewriterText :content="dog.name" /></h2>
      <a :href="`https://www.dogshome.org.au/our-dogs/${dog.id}`" target="_blank"
        ><span>Learn more</span><i class="pi pi-external-link" style="margin: 0"></i
      ></a>
      <p><span class="card__header-label">gender: </span>{{ dog.gender }}</p>
      <p><span class="card__header-label">age: </span>{{ formatAge(dog.age) }}</p>
      <p><span class="card__header-label">breed: </span>{{ dog.breed }}</p>
      <p><span class="card__header-label">size: </span>{{ dog.size }}</p>
      <p><span class="card__header-label">adoption fee: </span>AUD $ {{ dog.adoption_fee }}</p>
    </div>
    <div class="card__tags">
      <span v-for="tag in dog.tags" :key="tag" class="card__tag">
        {{ tag }}
      </span>
    </div>
    <div class="card__footer">
      <p>{{ dog.description }}</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { DogResponse } from '@/types/DogResponse'
import TypewriterText from './TypewriterText.vue'
const props = defineProps<{
  dog: DogResponse
}>()

function formatAge(age: number): string {
  if (age < 1) {
    return '< 1 years'
  } else if (age === 1) {
    return '1 year'
  } else {
    return age + ' years'
  }
}
</script>

<style scoped>
.card {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);

  border-radius: var(--radius-lg);
  padding: var(--space-2);
  max-width: 100%;
}

.card__header {
  display: grid;
  grid-template-columns: 1fr;
  justify-items: start;
  justify-content: space-between;
  gap: var(--space-1);
}

@media (min-width: 768px) {
  .card__header {
    grid-template-columns: repeat(2, max-content);
  }
}

.card__header-label {
  font-weight: 600;
}

.card__header a {
  text-decoration: none;
  background-color: var(--clr-dark);
  border-radius: var(--radius-md);
  padding: var(--space-1) var(--space-2);
  color: var(--clr-font);
  transition: background-color 0.2s ease;

  display: flex;
  align-items: center;
  gap: var(--space-1);
}

.card__header a:hover {
  filter: brightness(85%);
}

.card__header p {
  text-transform: capitalize;
}

.card__tags {
  display: flex;
  gap: var(--space-1);
  flex-wrap: wrap;
}

.card__tag {
  background-color: var(--clr-dark);
  filter: opacity(75%);
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-pill);
}

.card__header,
.card__footer {
  color: var(--clr-dark);
  font-size: var(--font-p-lg);
}
</style>
