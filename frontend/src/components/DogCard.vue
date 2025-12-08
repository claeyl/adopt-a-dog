<template>
  <section class="card">
    <div class="card__header">
      <h3>{{ dog.name }}</h3>
      <a :href="`https://www.dogshome.org.au/our-dogs/${dog.id}`" target="_blank"
        >Learn more about me</a
      >
      <p>{{ dog.gender }}</p>
      <p>{{ dog.age }} years</p>
      <p>{{ dog.breed }}</p>
      <p>{{ dog.size }}</p>
      <p>AUD $ {{ dog.adoptionFee }}</p>
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
const props = defineProps<{
  dog: DogResponse
}>()
</script>

<style scoped>
.card {
  border: solid 1px var(--color-surface-100);
  border-radius: 1rem;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.card__header {
  display: grid;
  grid-template-columns: repeat(2, max-content);
  justify-content: space-between;
  gap: 0.5rem;
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
}

.card__header a:hover {
  background-color: var(--color-secondary-dark);
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

.card__footer p {
  line-height: 1.5;
}
</style>
