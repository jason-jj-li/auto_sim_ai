"""Synthetic persona generation from statistical distributions."""
import random
import numpy as np
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

