import { ref } from 'vue';
import axios from 'axios';

const chunkArray = (array, size) => {
    const chunked = [];
    for (let i = 0; i < array.length; i += size) {
        chunked.push(array.slice(i, i + size));
    }
    return chunked;
};

const fetchProfessionals = () => {
    const professionals = ref([]);
    const chunkedProfessionals = ref([]);
    const professionalError = ref(null)

    const loadProfessionals = async (searchQuery = '', filterBy = '') => {
        try {
            if (searchQuery && filterBy) {
                var response = await axios.get("http://localhost:5000/api/filter-users", {
                    params: {
                        filter_by: filterBy,    
                        search_query: searchQuery
                    }
                });
            } else {
                var response = await axios.get("http://localhost:5000/api/professionals");
            }

            if(!response.data){
                throw Error('No professionals available')
            }
            professionals.value = response.data;
            chunkedProfessionals.value = chunkArray(professionals.value, 4);
        } 
        catch (error) {
            professionalError.value = error.message
        }
    };

    return { professionals, chunkedProfessionals, professionalError, loadProfessionals }
};

export default fetchProfessionals;