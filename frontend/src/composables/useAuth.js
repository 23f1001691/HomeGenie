import { useRouter } from "vue-router";
import { useStore } from "vuex";
import { ref } from "vue";
import axios from "axios";

const useAuth = () => {
    const store = useStore();
    const router = useRouter();
    const error = ref('');
    const showError = ref(false)

    const logOutUser = async (showDropdown) => {
        
        try {
            const response = await axios.post("http://127.0.0.1:5000/auth/logout");
            console.log(response.data.message)
            store.dispatch("logOut");
        } 
        catch (err) {
            error.value = 'Error logging out.'
            showError.value = true
        }

        if (showDropdown) {
            showDropdown.value = false; 
        }

        router.push({ name : 'Login' });
    };

  return { error, showError, logOutUser };
};

export default useAuth;
