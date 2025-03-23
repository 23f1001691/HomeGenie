import { ref } from 'vue';
import axios from 'axios';

const chunkArray = (array, size) => {
    const chunked = [];
    for (let i = 0; i < array.length; i += size) {
        chunked.push(array.slice(i, i + size));
    }
    return chunked;
};

const fetchCategories = () => {
    const categories = ref([]);
    const chunkedCategories = ref([]);
    const categoryError = ref(null)
    
    const loadCategories = async () => {
        try {
            const response = await axios.get("http://localhost:5000/api/categories");
            
            if(!response.data){
                throw Error('No categories available')
            }

            categories.value = response.data;
            chunkedCategories.value = chunkArray(categories.value, 4);
        } 
        catch (error) {
            categoryError.value = error.message
        }
    };

    return { chunkedCategories, categoryError, loadCategories }
};

export default fetchCategories;