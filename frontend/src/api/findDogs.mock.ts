import type { DogInfoResponse } from '@/types/DogInfoResponse'
import type { HttpError } from '@/types/Error'

const mockData = {
  results: [
    {
      id: 23316,
      name: 'Cadbury',
      gender: 'female',
      age: 3.0,
      breed: 'medium mixed breed',
      size: 'medium',
      weight: 28.0,
      adoptionFee: 590.0,
      tags: ['older children', 'calm home needed'],
      description:
        'Cadbury is a nice staffy girl who is looking for her forever home. She would do best as the only dog in the home. She will need up to 1hr of exercise and enrichment each day. Cadbury could go home with polite kids 10+, pending a meet. She would benefit from a positive reinforcement trainer to help her new owners get off on the right foot. Cadbury will need to learn to trust that her new owners will advocate for her space. E.g. not allowing dogs to approach on lead. Cadbury will need up to 1hr of exercise and mental enrichment each day. New owners should focus on bonding and enrichment in the home the first few weeks and then progress to outside walkies. Come meet Cadbury today!',
      explanation:
        'Based on your preference for a family-friendly dog, Bella is an excellent match. Golden Retrievers are known for their gentle temperament and patience with children, making her ideal for households with kids. Golden Retrievers are known for their gentle temperament and patience with children, making her ideal for households with kids lorem ipsum dolor ipsum dor al et sit.',
    },
    {
      id: 23314,
      name: 'Simba',
      gender: 'female',
      age: 2.0,
      breed: 'medium mixed breed',
      size: 'medium',
      weight: 26.0,
      adoptionFee: 590.0,
      tags: ['behavior training needed', 'older children', 'dog friendly'],
      description:
        "Meet Simba - a loving, energetic girl with a big heart! Simba can be a little unsure around new dogs at first but, with gentle introductions, she enjoys playtime and companionship. She's a clever, affectionate girl who's looking for a calm, experienced home where she can build confidence and learn at her own pace. Simba would love a doggy brother who can help show her the ropes and keep her company when her people are away. She's best suited to a home with dog-savvy kids aged 10+ who understand she may need space when feeling overwhelmed. With time, love, and patient training, Simba will make a wonderful, loyal companion.",
      explanation:
        'Based on your preference for a family-friendly dog, Bella is an excellent match. Golden Retrievers are known for their gentle temperament and patience with children, making her ideal for households with kids. Golden Retrievers are known for their gentle temperament and patience with children, making her ideal for households with kids lorem ipsum dolor ipsum dor al et sit.',
    },
    {
      id: 23426,
      name: 'Palm',
      gender: 'female',
      age: 0.0,
      breed: 'shar pei',
      size: 'medium',
      weight: 0.0,
      adoptionFee: 790.0,
      tags: [],
      description:
        'This pup will need a fun loving family environment where they can be adequately socialised and integrated to their new lifestyle through rewarding experiences ★ Part / flexible work hours are required so puppy behaviours and needs can be managed accordingly over the first few months. They must be given lots of new opportunities to meet & play with other friendly dogs whilst in controlled situation. Mandatory puppy classes will assist with this and set pup up for success in their new life.  My new Paw-rents must be committed to providing adequate exercise and enrichment! This puppy will be suitable to live with children as long as parents understand the time and effort demands of having a young puppy -`♡´-',
      explanation:
        'Based on your preference for a family-friendly dog, Bella is an excellent match. Golden Retrievers are known for their gentle temperament and patience with children, making her ideal for households with kids. Golden Retrievers are known for their gentle temperament and patience with children, making her ideal for households with kids lorem ipsum dolor ipsum dor al et sit.',
    },
    {
      id: 23372,
      name: 'Aang',
      gender: 'male',
      age: 0.0,
      breed: 'american staffordshire bull terrier',
      size: 'medium',
      weight: 8.0,
      adoptionFee: 790.0,
      tags: [],
      description:
        'Lovely little Aang is a sweet pup who is looking for his forever home. He can be unsure of the big wide world, but quickly learns its safe if people go at his pace. This little one would make his family very happy, he could go home with calm kids 10+ pending a meet. This little guy MUST go home with a mature, older doggy sibling to show him the ropes 🙂 Group training is also mandatory for this young boy. Please enquire about him today!',
      explanation:
        'Based on your preference for a family-friendly dog, Bella is an excellent match. Golden Retrievers are known for their gentle temperament and patience with children, making her ideal for households with kids. Golden Retrievers are known for their gentle temperament and patience with children, making her ideal for households with kids lorem ipsum dolor ipsum dor al et sit.',
    },
    {
      id: 23361,
      name: 'Antman',
      gender: 'male',
      age: 0.0,
      breed: 'medium mixed breed',
      size: 'medium',
      weight: 1.35,
      adoptionFee: 790.0,
      tags: ['behavior training needed', 'children', 'dog friendly'],
      description:
        'Lovely little Aang is a sweet pup who is looking for his forever home. He can be unsure of the big wide world, but quickly learns its safe if people go at his pace. This little one would make his family very happy, he could go home with calm kids 10+ pending a meet. This little guy MUST go home with a mature, older doggy sibling to show him the ropes 🙂 Group training is also mandatory for this young boy. Please enquire about him today!',
      explanation:
        'Based on your preference for a family-friendly dog, Bella is an excellent match. Golden Retrievers are known for their gentle temperament and patience with children, making her ideal for households with kids. Golden Retrievers are known for their gentle temperament and patience with children, making her ideal for households with kids lorem ipsum dolor ipsum dor al et sit.',
    },
  ],
}

export async function mockFindDogs(error?: HttpError): Promise<DogInfoResponse[]> {
  // mock latency
  await new Promise((r) => setTimeout(r, 3000))

  if (error) {
    throw error
  }
  return mockData.results
}
