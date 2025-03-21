import { ref } from 'vue';
import axios from 'axios';

const chunkArray = (array, size) => {
    const chunked = [];
    for (let i = 0; i < array.length; i += size) {
        chunked.push(array.slice(i, i + size));
    }
    return chunked;
};

const fetchCustomers = () => {
    const customers = ref([]);
    const chunkedCustomers = ref([]);
    const customerError = ref(null)
    
    const loadCustomers = async (searchQuery = '', filterBy = '') => {
        try {
            if (searchQuery && filterBy) {
                var response = await axios.get("http://localhost:5000/api/filter-users", {
                    params: {
                        filter_by: filterBy,    
                        search_query: searchQuery
                    }
                });
            } else {
                var response = await axios.get("http://localhost:5000/api/customers");
            }
            
            if(!response.data){
                throw Error('No customers available')
            }

            customers.value = response.data;
            chunkedCustomers.value = chunkArray(customers.value, 4);
        } 
        catch (error) {
            customerError.value = error.message
        }
    };

    return { chunkedCustomers, customerError, loadCustomers }
};

export default fetchCustomers;