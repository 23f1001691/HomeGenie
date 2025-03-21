import { ref } from 'vue';

const useCarousel = () => {
    const currentIndex = ref(0);

    const showSlide = (index, items) => {
        if (index < 0) {
            currentIndex.value = 0;
        } else if (index >= items.length) {
            currentIndex.value = items.length - 1;
        } else {
            currentIndex.value = index;
        }
    };

    const nextSlide = (items) => {
        if (currentIndex.value < items.length - 1) {
            showSlide(currentIndex.value + 1, items);
        }
    };

    const prevSlide = (items) => {
        if (currentIndex.value > 0) {
            showSlide(currentIndex.value - 1, items);
        }
    };

    return { currentIndex, nextSlide, prevSlide, showSlide };
}

export default useCarousel;