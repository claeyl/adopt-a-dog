import type { DogInfoResponse } from '@/types/DogInfoResponse'
import type { HttpError } from '@/types/Error'

const mockData = {
  results: [
    {
      id: 22067,
      name: 'Rubix',
      imageUrl:
        'https://www.dogshome.org.au/wp-content/uploads/2025/01/ea87ef70645141e8a688c97fca70f32c-1738290053-1738290053-jpeg-scaled.jpeg',
      gender: 'male',
      age: 5.0,
      breed: 'shar pei',
      size: 'medium',
      weight: 22.2,
      adoptionFee: 590.0,
      tags: ['no children', 'calm home needed', 'choosy with dog friends'],
      description:
        'Rubix is a handsome little boy who is in need of his furever home. He is a friendly & affectionate boy once he gets to know you & has really good manners, knows basic skills and is a motivated learner. Toy time is his favourite 🙂 Rubix will need some help & guidance but has been steadily improving his dog reactivity, his new owners will need to understand his Training and management going forward. He is best in an adult only home and is not really suited to novice dog owners. Rubix is sure to bond strongly with his new family and will be a devoted doggo companion.',
      explanation:
        'Although Rubix is friendly and affectionate, he requires experienced handling due to his reactivity and specific needs, making him better suited for owners with prior dog care experience rather than first-time owners. His behavior and training requirements suggest a level of expertise that a novice may find challenging to manage.',
    },
    {
      id: 22272,
      name: 'Leelo',
      imageUrl:
        'https://www.dogshome.org.au/wp-content/uploads/2025/03/2c874480471c4dcca0db78ac4efd61fc-1742443775-1742443775-jpg-scaled.jpg',
      gender: 'female',
      age: 6.0,
      breed: 'alaskan malamute',
      size: 'large',
      weight: 39.8,
      adoptionFee: 590.0,
      tags: ['dog friendly', 'teenagers'],
      description:
        'Lovely Leelo is a happy fluffy gal who is looking for a loving and dedicated home. This lady would enjoy having dog friends in her next home, and may be suited to living with dog savvy teens 13+. Leelo is a big bundle of love, she can be jumpy but just wants to say hi. Owners who are familiar with her breed/mix would be best – and hope you don’t mind dog hair as she has lots to share!! This girl will make an amazing companion, please enquire about her today!',
      explanation:
        'Leelo is a friendly and affectionate Alaskan Malamute who is great with other dogs and teens aged 13+, making her a good fit for first-time owners with some dog experience. Her loving nature and compatibility with dog-savvy households suggest she can thrive in a committed, beginner-friendly environment.',
    },
    {
      id: 23608,
      name: 'Noelle',
      imageUrl:
        'https://www.dogshome.org.au/wp-content/uploads/2025/12/25208144443f44a6a38066aa99c7a88e-1766725870-1766725901-jpeg.jpeg',
      gender: 'female',
      age: 2.0,
      breed: 'large mixed breed',
      size: 'large',
      weight: 0.0,
      adoptionFee: 590.0,
      tags: ['behavior training needed', 'older children'],
      description:
        'Noelle is a sweet girl who is looking for her new home. This girl loves to stretch her legs and would love daily exercise with her owners. She can make dog friends but can get over excited when she sees them, she has potential to live with a nice doggy brother pending a meet. Noelle is a sweetheart and could potentially live with dog savvy kids 10+ as long as they like her goofy side! Please enquire about this cutie today.',
      explanation:
        'Noelle is a sweet and affectionate large dog who is ideal for first-time owners due to her loving nature and manageable energy level with proper daily exercise. While some training may be needed, her enthusiasm for people and potential to get along with kids 10+ and other dogs makes her a great fit for a new, committed owner ready for a gentle, fun companion.',
    },
    {
      id: 23314,
      name: 'Simba',
      imageUrl: '',
      gender: 'female',
      age: 2.0,
      breed: 'medium mixed breed',
      size: 'medium',
      weight: 26.0,
      adoptionFee: 590.0,
      tags: ['behavior training needed', 'older children', 'dog friendly'],
      description:
        'Meet Simba – a loving, energetic girl with a big heart! Simba can be a little unsure around new dogs at first but, with gentle introductions, she enjoys playtime and companionship. She’s a clever, affectionate girl who’s looking for a calm, experienced home where she can build confidence and learn at her own pace. Simba would love a doggy brother who can help show her the ropes and keep her company when her people are away. She’s best suited to a home with dog-savvy kids aged 10+ who understand she may need space when feeling overwhelmed. With time, love, and patient training, Simba will make a wonderful, loyal companion.',
      explanation:
        'Simba is well-suited for first-time owners due to her affectionate nature and potential for growth with patience and guidance. Her need for gentle training and a calm environment aligns with the learning curve of new pet parents, while her dog-friendly disposition can aid in socialization and provide comfort in a household with another pet.',
    },
    {
      id: 23420,
      name: 'Bessy',
      imageUrl:
        'https://www.dogshome.org.au/wp-content/uploads/2025/12/53d4874356c947278eac1151982e839a-1766294517-176630032-jpg.jpg', // deliberate malformed URL
      gender: 'female',
      age: 6.0,
      breed: 'shar pei',
      size: 'medium',
      weight: 0.0,
      adoptionFee: 590.0,
      tags: ['older children', 'calm home needed', 'dog friendly'],
      description:
        'Bessy is a gentle friendly soul who is looking to become a beloved companion dog. She is sweet, affectionate and enjoys sniffing and exploring new things and being spoilt by her humans. Bessy is good with other polite friendly Doggo’s she does want well mannered pooches however as is a 6 y/o with a breeding history who gets fed up with excited rude Doggos in her face. She may suit a family home with kids, Bessy is so lovely and will make a wonderful family member she deserves the best.',
      explanation:
        'Bessy is an ideal choice for first-time owners due to her sweet, calm, and affectionate nature. She is experienced being around kids and other well-mannered dogs, making her easy to manage in a family setting. Her gentle personality and adaptability help ensure a smooth and enjoyable experience for new dog owners.',
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
