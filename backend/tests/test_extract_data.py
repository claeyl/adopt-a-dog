import unittest

from populate_db.extract_data import parse_basic_dog_info

class TestParseBasicDogInfo(unittest.TestCase):
  def test_complete_info(self):
    raw_text = "Evie\nID: 23515\nApply to Adopt Me\nFemale\n3 Years & 1 Months & 1 Week\nMastiff\nLarge                    (44 kg)\nFee:\n$590 AUD\nVaccinated:\nDesexed:\nMicrochipped:"
    res = parse_basic_dog_info(raw_text)
    id, name, gender, age, breed, size, weight, adoption_fee = res
    
    self.assertEqual(id, 23515)
    self.assertEqual(name, 'Evie')
    self.assertEqual(gender, 'female')
    self.assertEqual(age, 3)
    self.assertEqual(breed, 'mastiff')
    self.assertEqual(size, 'large')
    self.assertEqual(weight, 44.0)
    self.assertEqual(adoption_fee, 590.0)

  def test_incomplete_age(self):
    raw_text = "Aang\nID: 23372\nApply to Adopt Me\nMale\n6 Months &\nAmerican Staffordshire Bull Terrier\nMedium                    (8 kg)\nFee:\n$590 AUD\nVaccinated:\nDesexed:\nMicrochipped:"
    res = parse_basic_dog_info(raw_text)
    id, name, gender, age, breed, size, weight, adoption_fee = res
    
    self.assertEqual(id, 23372)
    self.assertEqual(name, 'Aang')
    self.assertEqual(gender, 'male')
    self.assertEqual(age, 0)
    self.assertEqual(breed, 'american staffordshire bull terrier')
    self.assertEqual(size, 'medium')
    self.assertEqual(weight, 8.0)
    self.assertEqual(adoption_fee, 590.0)
