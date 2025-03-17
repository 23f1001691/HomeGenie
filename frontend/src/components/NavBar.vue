<template>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <router-link :to="{ name : 'Home' }" class="navbar-brand">HomeGenie</router-link> 
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo02"
                aria-controls="navbarTogglerDemo02" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarTogglerDemo02">
                <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
                    <li class="nav-item px-3">
                        <router-link :to="{ name : 'Login' }" class="nav-link">Login</router-link> 
                    </li>
                    <li class="nav-item px-3">
                        <router-link :to="{ name : 'Signup' }" class="nav-link">Sign Up</router-link> 
                    </li>
                </ul>
            </div>
        </div>
    </nav>
</template>

<script>
export default {
  name: 'NavBar'
}
</script>