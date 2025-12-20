<template>
  <section class="card">
    <div class="card__header">
      <h3><TypewriterText :content="dog.name" /></h3>
      <a :href="`https://www.dogshome.org.au/our-dogs/${dog.id}`" target="_blank"
        ><span>Learn more about me</span><i class="pi pi-external-link" style="margin: 0"></i
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
  border: solid 1px var(--color-surface-200);
  border-radius: 1rem;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.card__header {
  display: grid;
  grid-template-columns: repeat(2, max-content);
  justify-content: space-between;
  gap: 0.5rem;
}

.card__header-label {
  font-weight: 600;
}

.card__header h3 {
  font-size: 1.75rem;
}

.card__header a {
  text-decoration: none;
  background-color: var(--color-secondary);
  border-radius: 0.25rem;
  padding: 0.5rem 1rem;
  color: inherit;
  transition: background-color 0.2s ease;

  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.card__header a:hover {
  background-color: var(--color-secondary-dark);
}

.card__header p {
  text-transform: capitalize;
}

.card__tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.card__tag {
  background-color: var(--color-surface-100);
  padding: 0.4rem 1rem;
  border-radius: 9999px;
}
</style>
