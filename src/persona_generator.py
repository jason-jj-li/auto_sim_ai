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
                persona['background'] = self._generate_background(persona)
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
    
    def _generate_background(self, persona: Dict[str, Any]) -> str:
        """
        Generate a coherent background narrative based on persona attributes.
        
        Args:
            persona: Dictionary containing persona attributes
            
        Returns:
            A narrative background string
        """
        background_parts = []
        
        # Basic demographic info
        age = persona.get('age', 30)
        gender = persona.get('gender', 'Person')
        occupation = persona.get('occupation', 'Worker')
        
        # Education background
        education = persona.get('education')
        if education:
            edu_map = {
                '文盲': '没有接受过正规教育',
                '小学': '接受过小学教育',
                '初中': '拥有初中学历',
                '高中': '高中毕业',
                '本科': '拥有本科学历',
                '硕士': '拥有硕士学位',
                '博士': '拥有博士学位'
            }
            edu_desc = edu_map.get(education, f'教育程度为{education}')
            background_parts.append(edu_desc)
        
        # Occupation and career stage
        if age < 25:
            background_parts.append(f'目前从事{occupation}工作，处于职业生涯早期阶段')
        elif age < 45:
            background_parts.append(f'是一名{occupation}，正值职业发展的黄金时期')
        elif age < 65:
            background_parts.append(f'从事{occupation}工作多年，拥有丰富的工作经验')
        else:
            background_parts.append(f'曾长期从事{occupation}工作，现已退休或接近退休')
        
        # Marital status and family
        marital = persona.get('marital_status')
        if marital:
            marital_map = {
                '未婚': '目前单身',
                '已婚': '已婚，与配偶共同生活',
                '离异': '经历过婚姻，现已离异',
                '丧偶': '配偶已故'
            }
            marital_desc = marital_map.get(marital, marital)
            background_parts.append(marital_desc)
        
        # Location and living environment
        location = persona.get('location')
        if location:
            if location == '城镇' or '城镇' in str(location):
                background_parts.append('居住在城镇地区，生活便利')
            elif location == '农村' or '农村' in str(location):
                background_parts.append('生活在农村地区，保持着传统的生活方式')
            else:
                background_parts.append(f'居住在{location}')
        
        # Ethnicity
        ethnicity = persona.get('ethnicity')
        if ethnicity and ethnicity != '汉族':
            background_parts.append(f'民族身份为{ethnicity}')
        
        # Political affiliation
        political = persona.get('political_affiliation')
        if political:
            if political == '中共党员':
                background_parts.append('是中国共产党党员')
            elif political == '共青团员':
                background_parts.append('是共青团员')
            elif political == '民主党派':
                background_parts.append('参加了民主党派')
        
        # Religion
        religion = persona.get('religion')
        if religion and religion not in ['无宗教信仰', '无神论']:
            background_parts.append(f'信仰{religion}')
        
        # Add other custom attributes
        for var_name, value in persona.items():
            if var_name not in ['name', 'age', 'gender', 'occupation', 'background',
                                'personality_traits', 'values', 'education', 'marital_status',
                                'location', 'ethnicity', 'political_affiliation', 'religion']:
                if value and str(value).strip():
                    # Format the attribute name
                    var_display = var_name.replace('_', ' ').title()
                    background_parts.append(f'{var_display}: {value}')
        
        return '。'.join(background_parts) + '。' if background_parts else ''
    
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
            
            # Try to extract percentages from the gender string
            # Pattern: "Male (51.24%), Female (48.76%)" or "Male: 51.24%, Female: 48.76%"
            import re
            male_match = re.search(r'male[:\s]*\(?(\d+\.?\d*)\s*%', gender_str, re.IGNORECASE)
            female_match = re.search(r'female[:\s]*\(?(\d+\.?\d*)\s*%', gender_str, re.IGNORECASE)
            
            if male_match and female_match:
                # Both percentages found - use exact values
                male_pct = float(male_match.group(1)) / 100.0
                female_pct = float(female_match.group(1)) / 100.0
                
                # Normalize if they don't add up to 1.0
                total = male_pct + female_pct
                if total > 0:
                    male_pct = male_pct / total
                    female_pct = female_pct / total
                
                generator.add_distribution(DistributionConfig(
                    'gender', 'categorical',
                    {'categories': ['Male', 'Female'],
                     'probabilities': [male_pct, female_pct]}
                ))
            elif 'mixed' in gender_str or 'both' in gender_str or 'all' in gender_str:
                # Mixed gender - default 50/50
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
        
        # Parse education levels from descriptive text
        education_info = extracted_data.get('education')
        if education_info and isinstance(education_info, str):
            education_str = str(education_info).lower()
            education_levels = []
            education_weights = []
            
            # Common education levels with default weights
            edu_map = {
                '文盲': 0.03,
                '小学': 0.08,
                '初中': 0.20,
                '高中': 0.18,
                '本科': 0.35,
                '硕士': 0.12,
                '博士': 0.04
            }
            
            # Check if the text indicates a range (涵盖/包括/从...到...)
            has_range = any(keyword in education_str for keyword in ['涵盖', '包括', '从', '到', '至'])
            
            # If it's a range description, include all levels
            if has_range:
                for level in edu_map.keys():
                    education_levels.append(level)
                    weight = edu_map[level]
                    
                    # Boost weights for levels mentioned with "为主"
                    if '为主' in education_str:
                        if level in education_str:
                            weight *= 1.8
                    
                    education_weights.append(weight)
            else:
                # Only include specifically mentioned levels
                for level in edu_map.keys():
                    if level in education_str:
                        education_levels.append(level)
                        weight = edu_map[level]
                        
                        if '为主' in education_str:
                            weight *= 1.8
                        
                        education_weights.append(weight)
            
            # If any levels found, use them
            if education_levels:
                # Normalize weights
                total_weight = sum(education_weights)
                education_probs = [w/total_weight for w in education_weights]
                
                generator.add_distribution(DistributionConfig(
                    'education', 'categorical',
                    {'categories': education_levels, 'probabilities': education_probs}
                ))
        
        # Parse location - extract urban/rural distribution
        location_info = extracted_data.get('location')
        if location_info and isinstance(location_info, str):
            location_str = str(location_info)
            
            # Try to extract percentages for urban/rural
            import re
            urban_match = re.search(r'城镇[居民]*[占]*\s*(\d+\.?\d*)\s*%', location_str)
            rural_match = re.search(r'农村[居民]*[占]*\s*(\d+\.?\d*)\s*%', location_str)
            
            if urban_match and rural_match:
                urban_pct = float(urban_match.group(1)) / 100.0
                rural_pct = float(rural_match.group(1)) / 100.0
                
                # Normalize
                total = urban_pct + rural_pct
                if total > 0:
                    urban_pct = urban_pct / total
                    rural_pct = rural_pct / total
                
                generator.add_distribution(DistributionConfig(
                    'location', 'categorical',
                    {'categories': ['城镇', '农村'], 'probabilities': [urban_pct, rural_pct]}
                ))
        
        # Parse marital status
        marital_info = extracted_data.get('marital_status')
        if marital_info and isinstance(marital_info, str):
            marital_str = str(marital_info)
            marital_statuses = []
            marital_weights = []
            
            marital_map = {
                '未婚': 0.20,
                '已婚': 0.60,
                '离异': 0.10,
                '丧偶': 0.10
            }
            
            for status, weight in marital_map.items():
                if status in marital_str:
                    marital_statuses.append(status)
                    # Increase weight if marked as primary
                    if '为主' in marital_str and status == '已婚':
                        weight *= 2.0
                    marital_weights.append(weight)
            
            if marital_statuses:
                total_weight = sum(marital_weights)
                marital_probs = [w/total_weight for w in marital_weights]
                
                generator.add_distribution(DistributionConfig(
                    'marital_status', 'categorical',
                    {'categories': marital_statuses, 'probabilities': marital_probs}
                ))
        
        # Parse ethnicity
        ethnicity_info = extracted_data.get('ethnicity')
        if ethnicity_info and isinstance(ethnicity_info, str):
            ethnicity_str = str(ethnicity_info)
            
            # Extract percentage for 汉族
            import re
            han_match = re.search(r'汉族[^\d]*(\d+)\s*%', ethnicity_str)
            minority_match = re.search(r'少数民族[^\d]*(\d+\.?\d*)\s*[-~]?\s*(\d+\.?\d*)\s*%', ethnicity_str)
            
            han_pct = 0.90  # default
            if han_match:
                han_pct = float(han_match.group(1)) / 100.0
            
            # Create distribution
            ethnicities = ['汉族']
            probs = [han_pct]
            
            # Add some minority groups if mentioned
            minorities = ['壮族', '回族', '满族', '维吾尔族', '藏族']
            found_minorities = [m for m in minorities if m in ethnicity_str]
            
            if found_minorities:
                minority_pct = 1.0 - han_pct
                per_minority = minority_pct / len(found_minorities)
                ethnicities.extend(found_minorities)
                probs.extend([per_minority] * len(found_minorities))
            
            generator.add_distribution(DistributionConfig(
                'ethnicity', 'categorical',
                {'categories': ethnicities, 'probabilities': probs}
            ))
        
        # Parse political affiliation
        political_info = extracted_data.get('political_affiliation')
        if political_info and isinstance(political_info, str):
            political_str = str(political_info)
            
            political_groups = []
            political_weights = []
            
            political_map = {
                '群众': 0.60,
                '中共党员': 0.25,
                '共青团员': 0.10,
                '民主党派': 0.03,
                '无党派': 0.02
            }
            
            for group, weight in political_map.items():
                if group in political_str or (group == '中共党员' and '党员' in political_str):
                    political_groups.append(group)
                    if '为主' in political_str and group == '群众':
                        weight *= 1.5
                    political_weights.append(weight)
            
            if political_groups:
                total_weight = sum(political_weights)
                political_probs = [w/total_weight for w in political_weights]
                
                generator.add_distribution(DistributionConfig(
                    'political_affiliation', 'categorical',
                    {'categories': political_groups, 'probabilities': political_probs}
                ))
        
        # Parse religion
        religion_info = extracted_data.get('religion')
        if religion_info and isinstance(religion_info, str):
            religion_str = str(religion_info)
            
            religions = []
            religion_weights = []
            
            religion_map = {
                '无宗教信仰': 0.70,
                '佛教': 0.10,
                '道教': 0.05,
                '基督教': 0.05,
                '伊斯兰教': 0.05,
                '无神论': 0.05
            }
            
            for religion, weight in religion_map.items():
                if religion in religion_str:
                    religions.append(religion)
                    if '为主' in religion_str and religion == '无宗教信仰':
                        weight *= 2.0
                    religion_weights.append(weight)
            
            if religions:
                total_weight = sum(religion_weights)
                religion_probs = [w/total_weight for w in religion_weights]
                
                generator.add_distribution(DistributionConfig(
                    'religion', 'categorical',
                    {'categories': religions, 'probabilities': religion_probs}
                ))
        
        # Add other demographic attributes as custom distributions
        for key, value in extracted_data.items():
            if key in ['age', 'age_range', 'gender', 'error', 'raw_response', 'sample_size',
                       'education', 'location', 'marital_status', 'ethnicity', 
                       'political_affiliation', 'religion']:
                # Skip already processed fields
                continue
            
            if value is None:
                continue
            
            # If it's a list, use categorical distribution
            if isinstance(value, list) and value:
                generator.add_distribution(DistributionConfig(
                    key, 'categorical',
                    {'categories': value}
                ))
            # If it's a string, store as-is (will be added to background)
            elif isinstance(value, str):
                # Don't create distribution for descriptive strings
                # They will be added to persona background later
                pass
        
        # Generate personas
        personas = generator.generate_personas(
            n=n,
            include_background=True,
            include_traits=True,
            include_values=True
        )
        
        # Enhance personas with extracted information
        for persona in personas:
            # Add interests and values from extracted data if present
            if extracted_data.get('interests') and isinstance(extracted_data['interests'], list):
                # Replace with AI-extracted interests
                persona['personality_traits'] = extracted_data['interests'][:3]
            
            if extracted_data.get('values') and isinstance(extracted_data['values'], list):
                # Replace values with extracted ones
                persona['values'] = extracted_data['values'][:5]
            
            # Enhance background with additional descriptive fields
            # The base background is already generated by _generate_background
            base_background = persona.get('background', '')
            additional_parts = []
            
            # Add income information if provided
            income_range = extracted_data.get('income_range')
            if income_range:
                if '2000-9999' in str(income_range) or '中等' in str(income_range):
                    additional_parts.append('收入水平属于中等收入群体')
                elif '低于2000' in str(income_range) or '低收入' in str(income_range):
                    additional_parts.append('收入水平相对较低')
                elif '20000以上' in str(income_range) or '高收入' in str(income_range):
                    additional_parts.append('属于高收入群体')
                else:
                    additional_parts.append(f'月收入在{income_range}')
            
            # Add family structure if provided
            family_structure = extracted_data.get('family_structure')
            if family_structure:
                if '2-4人' in str(family_structure):
                    additional_parts.append('与家人共同居住，家庭成员2-4人')
                elif '独居' in str(family_structure):
                    additional_parts.append('独自居住')
                else:
                    additional_parts.append(f'家庭情况：{family_structure}')
            
            # Add children/elderly care info if provided
            children = extracted_data.get('children')
            if children:
                if '0-14岁' in str(children) and '65岁以上' in str(children):
                    additional_parts.append('家中既有未成年子女也有老年家属需要照顾')
                elif '0-14岁' in str(children):
                    additional_parts.append('家中有未成年子女需要照顾')
                elif '65岁以上' in str(children):
                    additional_parts.append('家中有老年家属需要照料')
            
            # Add health status if provided
            health_status = extracted_data.get('health_status')
            if health_status:
                if '慢性病' in str(health_status):
                    additional_parts.append('关注自身健康，注意慢性病管理')
                elif '健康' in str(health_status):
                    additional_parts.append('注重健康生活方式，保持规律作息')
                else:
                    additional_parts.append(f'健康状况：{health_status}')
            
            # Add tech usage if provided
            tech_usage = extracted_data.get('tech_usage')
            if tech_usage:
                age = persona.get('age', 40)
                education = persona.get('education', '')
                location = persona.get('location', '')
                
                # Determine tech proficiency based on demographics
                if age < 40 and ('本科' in education or '硕士' in education or '博士' in education):
                    additional_parts.append('熟练使用各类数字工具和AI应用')
                elif age < 50 and '城镇' in str(location):
                    additional_parts.append('具备基本的数字技能，会使用常见的互联网应用')
                elif age >= 60 or '农村' in str(location):
                    additional_parts.append('对新技术了解有限，主要使用传统方式')
                else:
                    additional_parts.append('正在逐步适应数字化生活方式')
            
            # Add insurance coverage if provided
            insurance = extracted_data.get('insurance_coverage')
            if insurance:
                if '医疗保险' in str(insurance) and '养老保险' in str(insurance):
                    additional_parts.append('拥有基本医疗保险和养老保险')
                elif '医疗保险' in str(insurance):
                    additional_parts.append('拥有基本医疗保险')
                elif '养老保险' in str(insurance):
                    additional_parts.append('参加了养老保险')
            
            # Combine base background with additional information
            if additional_parts:
                full_background = base_background + '。' + '。'.join(additional_parts) + '。'
            else:
                full_background = base_background
            
            persona['background'] = full_background.replace('。。', '。').strip()
        
        return personas


