"""Synthetic persona generation from statistical distributions."""
import random
import numpy as np
import json
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class DistributionConfig:
    """Configuration for a demographic distribution."""
    variable_name: str
    distribution_type: str  # 'normal', 'uniform', 'categorical', 'custom'
    parameters: Dict[str, Any]
    
    def sample(self, n: int = 1) -> List[Any]:
        """Sample n values from this distribution."""
        if self.distribution_type == 'normal':
            mean = self.parameters.get('mean', 0)
            std = self.parameters.get('std', 1)
            samples = np.random.normal(mean, std, n)
            # Round if integer type expected
            if self.parameters.get('integer', False):
                samples = np.round(samples).astype(int)
            return samples.tolist()
        
        elif self.distribution_type == 'uniform':
            low = self.parameters.get('low', 0)
            high = self.parameters.get('high', 1)
            samples = np.random.uniform(low, high, n)
            if self.parameters.get('integer', False):
                samples = np.round(samples).astype(int)
            return samples.tolist()
        
        elif self.distribution_type == 'categorical':
            categories = self.parameters.get('categories', [])
            probabilities = self.parameters.get('probabilities', None)
            if probabilities:
                # Normalize probabilities
                total = sum(probabilities)
                probabilities = [p/total for p in probabilities]
            return np.random.choice(categories, size=n, p=probabilities).tolist()
        
        elif self.distribution_type == 'custom':
            # User provides a list of values to sample from
            values = self.parameters.get('values', [])
            if not values:
                return [None] * n
            return random.choices(values, k=n)
        
        return [None] * n


class PersonaGenerator:
    """Generate synthetic personas from demographic distributions."""
    
    # Common name lists
    FIRST_NAMES_MALE = [
        "James", "John", "Robert", "Michael", "William", "David", "Richard", 
        "Joseph", "Thomas", "Christopher", "Daniel", "Matthew", "Anthony", "Mark"
    ]
    
    FIRST_NAMES_FEMALE = [
        "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan",
        "Jessica", "Sarah", "Karen", "Nancy", "Lisa", "Betty", "Margaret"
    ]
    
    FIRST_NAMES_NEUTRAL = [
        "Alex", "Jordan", "Taylor", "Casey", "Morgan", "Riley", "Jamie", 
        "Avery", "Quinn", "Dakota"
    ]
    
    LAST_NAMES = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
        "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
        "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
        "Lee", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez",
        "Lewis", "Robinson", "Walker", "Young", "Allen", "King", "Wright"
    ]
    
    OCCUPATIONS_BY_AGE = {
        (18, 25): ["Student", "Intern", "Retail Worker", "Barista", "Server", "Delivery Driver"],
        (25, 35): ["Software Engineer", "Teacher", "Nurse", "Accountant", "Sales Representative", 
                   "Marketing Specialist", "Designer", "Analyst"],
        (35, 50): ["Manager", "Director", "Consultant", "Engineer", "Professor", "Physician",
                   "Attorney", "Architect", "Business Owner"],
        (50, 65): ["Senior Manager", "Executive", "Consultant", "Professor", "Healthcare Administrator",
                   "Financial Advisor", "Retired Professional"],
        (65, 100): ["Retired Teacher", "Retired Engineer", "Retired Nurse", "Retired Business Owner",
                    "Volunteer", "Retiree"]
    }
    
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize persona generator.
        
        Args:
            seed: Random seed for reproducibility
        """
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        
        self.distributions: Dict[str, DistributionConfig] = {}
    
    def add_distribution(self, config: DistributionConfig):
        """Add a distribution configuration."""
        self.distributions[config.variable_name] = config
    
    def generate_name(self, gender: Optional[str] = None) -> str:
        """
        Generate a random name.
        
        Args:
            gender: 'male', 'female', or None for neutral
            
        Returns:
            Full name
        """
        if gender and gender.lower() in ['male', 'm', 'man']:
            first_name = random.choice(self.FIRST_NAMES_MALE)
        elif gender and gender.lower() in ['female', 'f', 'woman']:
            first_name = random.choice(self.FIRST_NAMES_FEMALE)
        else:
            first_name = random.choice(self.FIRST_NAMES_NEUTRAL)
        
        last_name = random.choice(self.LAST_NAMES)
        return f"{first_name} {last_name}"
    
    def generate_occupation(self, age: int) -> str:
        """
        Generate occupation based on age.
        
        Args:
            age: Person's age
            
        Returns:
            Occupation string
        """
        for (min_age, max_age), occupations in self.OCCUPATIONS_BY_AGE.items():
            if min_age <= age < max_age:
                return random.choice(occupations)
        return "Retired"
    
    def generate_personas(
        self,
        n: int,
        include_background: bool = True,
        include_traits: bool = True,
        include_values: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Generate n synthetic personas.
        
        Args:
            n: Number of personas to generate
            include_background: Whether to generate background text
            include_traits: Whether to generate personality traits
            include_values: Whether to generate values
            
        Returns:
            List of persona dictionaries
        """
        if 'age' not in self.distributions:
            # Default age distribution: normal(45, 15)
            self.add_distribution(DistributionConfig(
                'age',
                'normal',
                {'mean': 45, 'std': 15, 'integer': True}
            ))
        
        if 'gender' not in self.distributions:
            # Default gender distribution: 50/50
            self.add_distribution(DistributionConfig(
                'gender',
                'categorical',
                {'categories': ['Female', 'Male', 'Non-binary'], 
                 'probabilities': [0.48, 0.48, 0.04]}
            ))
        
        personas = []
        
        for i in range(n):
            persona = {}
            
            # Sample all distributions
            for var_name, dist in self.distributions.items():
                value = dist.sample(1)[0]
                persona[var_name] = value
            
            # Ensure required fields
            age = persona.get('age', 45)
            if age < 18:
                age = 18
            elif age > 100:
                age = 100
            persona['age'] = age
            
            gender = persona.get('gender', 'Female')
            persona['gender'] = gender
            
            # Generate name
            if 'name' not in persona:
                persona['name'] = self.generate_name(gender)
            
            # Generate occupation
            if 'occupation' not in persona:
                persona['occupation'] = self.generate_occupation(age)
            
            # Generate background
            if include_background:
                background_parts = []
                
                # Add custom variables to background
                for var_name, value in persona.items():
                    if var_name not in ['name', 'age', 'gender', 'occupation', 
                                        'background', 'personality_traits', 'values']:
                        background_parts.append(f"{var_name}: {value}")
                
                persona['background'] = "; ".join(background_parts) if background_parts else ""
            else:
                persona['background'] = ""
            
            # Generate personality traits
            if include_traits:
                traits = self._generate_personality_traits()
                persona['personality_traits'] = traits
            else:
                persona['personality_traits'] = []
            
            # Generate values
            if include_values:
                values = self._generate_values()
                persona['values'] = values
            else:
                persona['values'] = []
            
            personas.append(persona)
        
        return personas
    
    def _generate_personality_traits(self) -> List[str]:
        """Generate random personality traits."""
        trait_pairs = [
            ("Introverted", "Extroverted"),
            ("Analytical", "Intuitive"),
            ("Calm", "Anxious"),
            ("Cautious", "Adventurous"),
            ("Reserved", "Outgoing"),
            ("Practical", "Creative"),
            ("Organized", "Spontaneous")
        ]
        
        num_traits = random.randint(3, 5)
        selected_pairs = random.sample(trait_pairs, num_traits)
        
        traits = []
        for pair in selected_pairs:
            # Randomly choose one trait from each pair
            trait = random.choice(pair)
            traits.append(trait)
        
        return traits
    
    def _generate_values(self) -> List[str]:
        """Generate random values."""
        all_values = [
            "Family", "Career", "Health", "Education", "Financial security",
            "Personal growth", "Community", "Creativity", "Independence",
            "Tradition", "Adventure", "Honesty", "Compassion", "Achievement"
        ]
        
        num_values = random.randint(3, 5)
        return random.sample(all_values, num_values)
    
    def generate_from_template(
        self,
        template_name: str,
        n: int
    ) -> List[Dict[str, Any]]:
        """
        Generate personas from a predefined template.
        
        Args:
            template_name: Name of the template ('general_population', 'college_students', 
                          'seniors', 'working_professionals')
            n: Number of personas to generate
            
        Returns:
            List of persona dictionaries
        """
        self.distributions.clear()
        
        if template_name == 'general_population':
            self.add_distribution(DistributionConfig(
                'age', 'normal', {'mean': 45, 'std': 15, 'integer': True}
            ))
            self.add_distribution(DistributionConfig(
                'gender', 'categorical',
                {'categories': ['Female', 'Male', 'Non-binary'], 
                 'probabilities': [0.48, 0.48, 0.04]}
            ))
        
        elif template_name == 'college_students':
            self.add_distribution(DistributionConfig(
                'age', 'uniform', {'low': 18, 'high': 24, 'integer': True}
            ))
            self.add_distribution(DistributionConfig(
                'gender', 'categorical',
                {'categories': ['Female', 'Male', 'Non-binary'], 
                 'probabilities': [0.52, 0.45, 0.03]}
            ))
            self.add_distribution(DistributionConfig(
                'year', 'categorical',
                {'categories': ['Freshman', 'Sophomore', 'Junior', 'Senior'],
                 'probabilities': [0.28, 0.26, 0.24, 0.22]}
            ))
        
        elif template_name == 'seniors':
            self.add_distribution(DistributionConfig(
                'age', 'normal', {'mean': 72, 'std': 8, 'integer': True}
            ))
            self.add_distribution(DistributionConfig(
                'gender', 'categorical',
                {'categories': ['Female', 'Male'], 'probabilities': [0.55, 0.45]}
            ))
            self.add_distribution(DistributionConfig(
                'living_situation', 'categorical',
                {'categories': ['Independent', 'With family', 'Assisted living', 'Nursing home'],
                 'probabilities': [0.70, 0.15, 0.10, 0.05]}
            ))
        
        elif template_name == 'working_professionals':
            self.add_distribution(DistributionConfig(
                'age', 'normal', {'mean': 38, 'std': 10, 'integer': True}
            ))
            self.add_distribution(DistributionConfig(
                'gender', 'categorical',
                {'categories': ['Female', 'Male', 'Non-binary'], 
                 'probabilities': [0.47, 0.50, 0.03]}
            ))
            self.add_distribution(DistributionConfig(
                'career_stage', 'categorical',
                {'categories': ['Entry-level', 'Mid-level', 'Senior', 'Executive'],
                 'probabilities': [0.25, 0.40, 0.25, 0.10]}
            ))
        
        return self.generate_personas(n)
    
    @staticmethod
    def extract_demographics_with_ai(
        text_input: str,
        llm_client: Any,
        model: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Use AI to extract demographic information from free-form text.
        
        Args:
            text_input: Free-form text describing person(s) or population
            llm_client: LLM client instance (e.g., LMStudioClient)
            model: Model name to use (optional)
            
        Returns:
            Dictionary with extracted demographic information
        """
        prompt = f"""You are a demographic data extraction assistant. Extract key demographic information from the following text and return it in a structured JSON format.

Text to analyze:
{text_input}

Please extract the following information if available:
- age or age_range (e.g., "25-35", "45", "18-24")
- gender (e.g., "Male", "Female", "Non-binary", "Mixed")
- occupation or occupation_category (e.g., "Teacher", "Healthcare Worker", "Students")
- education (e.g., "High School", "Bachelor's", "Master's", "PhD")
- location or region (e.g., "New York", "Rural areas", "California")
- income or income_range (e.g., "$30,000-$50,000", "High income", "Low income")
- marital_status (e.g., "Single", "Married", "Divorced")
- children (e.g., "0", "1-2", "3+")
- ethnicity or race (if mentioned)
- health_status (e.g., "Good", "Fair", "Chronic conditions")
- political_affiliation (e.g., "Liberal", "Conservative", "Independent")
- religion (if mentioned)
- interests (list of interests)
- values (list of core values)
- sample_size (estimated number of people described, e.g., "50", "100-200")
- any other relevant demographic attributes

Return ONLY a valid JSON object with the extracted information. Use null for fields not mentioned in the text.

Example format:
{{
  "age_range": "25-35",
  "gender": "Mixed",
  "occupation": "Software Engineers",
  "education": "Bachelor's or higher",
  "location": "San Francisco Bay Area",
  "income_range": "$80,000-$150,000",
  "sample_size": "100",
  "interests": ["Technology", "Startups", "Innovation"],
  "values": ["Career growth", "Work-life balance", "Innovation"]
}}

JSON output:"""

        messages = [
            {"role": "system", "content": "You are a helpful demographic data extraction assistant. Always respond with valid JSON only."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            response = llm_client.chat_completion(
                messages=messages,
                temperature=0.3,  # Lower temperature for more consistent extraction
                max_tokens=1000,
                model=model
            )
            
            if not response:
                return {"error": "No response from AI"}
            
            # Try to parse JSON from response
            # Clean up response (remove markdown code blocks if present)
            response_clean = response.strip()
            if response_clean.startswith("```json"):
                response_clean = response_clean[7:]
            elif response_clean.startswith("```"):
                response_clean = response_clean[3:]
            if response_clean.endswith("```"):
                response_clean = response_clean[:-3]
            response_clean = response_clean.strip()
            
            # Parse JSON
            extracted_data = json.loads(response_clean)
            return extracted_data
            
        except json.JSONDecodeError as e:
            return {"error": f"Failed to parse AI response as JSON: {str(e)}", "raw_response": response}
        except Exception as e:
            return {"error": f"AI extraction failed: {str(e)}"}
    
    @staticmethod
    def generate_personas_from_ai_extraction(
        extracted_data: Dict[str, Any],
        n: int,
        seed: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate personas based on AI-extracted demographic information.
        
        Args:
            extracted_data: Dictionary with extracted demographic information
            n: Number of personas to generate
            seed: Random seed for reproducibility
            
        Returns:
            List of persona dictionaries
        """
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        
        generator = PersonaGenerator(seed=seed)
        
        # Parse age information
        age_info = extracted_data.get('age') or extracted_data.get('age_range')
        if age_info:
            age_str = str(age_info)
            if '-' in age_str:
                # Age range like "25-35"
                try:
                    min_age, max_age = map(int, age_str.split('-'))
                    generator.add_distribution(DistributionConfig(
                        'age', 'uniform', 
                        {'low': min_age, 'high': max_age, 'integer': True}
                    ))
                except:
                    # Default if parsing fails
                    generator.add_distribution(DistributionConfig(
                        'age', 'normal', {'mean': 40, 'std': 15, 'integer': True}
                    ))
            else:
                # Single age or age description
                try:
                    age_val = int(age_str)
                    generator.add_distribution(DistributionConfig(
                        'age', 'normal', 
                        {'mean': age_val, 'std': 5, 'integer': True}
                    ))
                except:
                    # Default
                    generator.add_distribution(DistributionConfig(
                        'age', 'normal', {'mean': 40, 'std': 15, 'integer': True}
                    ))
        
        # Parse gender information
        gender_info = extracted_data.get('gender')
        if gender_info:
            gender_str = str(gender_info).lower()
            if 'mixed' in gender_str or 'both' in gender_str or 'all' in gender_str:
                # Mixed gender
                generator.add_distribution(DistributionConfig(
                    'gender', 'categorical',
                    {'categories': ['Female', 'Male', 'Non-binary'],
                     'probabilities': [0.48, 0.48, 0.04]}
                ))
            elif 'female' in gender_str or 'woman' in gender_str:
                generator.add_distribution(DistributionConfig(
                    'gender', 'categorical',
                    {'categories': ['Female', 'Male'],
                     'probabilities': [0.85, 0.15]}  # Mostly female
                ))
            elif 'male' in gender_str or 'man' in gender_str:
                generator.add_distribution(DistributionConfig(
                    'gender', 'categorical',
                    {'categories': ['Male', 'Female'],
                     'probabilities': [0.85, 0.15]}  # Mostly male
                ))
        
        # Add other demographic attributes as custom distributions
        for key, value in extracted_data.items():
            if key in ['age', 'age_range', 'gender', 'error', 'raw_response', 'sample_size']:
                continue
            
            if value is None:
                continue
            
            # If it's a list, use categorical distribution
            if isinstance(value, list) and value:
                generator.add_distribution(DistributionConfig(
                    key, 'categorical',
                    {'categories': value}
                ))
            # If it's a string, create a single-value distribution
            elif isinstance(value, str):
                generator.add_distribution(DistributionConfig(
                    key, 'categorical',
                    {'categories': [value]}
                ))
        
        # Generate personas
        personas = generator.generate_personas(
            n=n,
            include_background=True,
            include_traits=True,
            include_values=True
        )
        
        # Enhance personas with extracted information
        for persona in personas:
            # Override with extracted specific values where applicable
            if extracted_data.get('occupation'):
                persona['occupation'] = extracted_data['occupation']
            if extracted_data.get('location'):
                persona['location'] = extracted_data['location']
            if extracted_data.get('education'):
                persona['education'] = extracted_data['education']
            
            # Add interests and values from extracted data if present
            if extracted_data.get('interests') and isinstance(extracted_data['interests'], list):
                # Mix AI-extracted interests with generated ones
                persona['interests'] = extracted_data['interests'][:3]  # Take top 3
            
            if extracted_data.get('values') and isinstance(extracted_data['values'], list):
                # Replace values with extracted ones
                persona['values'] = extracted_data['values'][:5]  # Take top 5
        
        return personas


