import { createStore } from "vuex";

export default createStore({
  state: {
    role: null,
    userID: null,
    isFirstSession:false
  },
  getters: {
    getRole(state) {
      return state.role;
    },
    getUserID(state) {
      return state.userID;
    },
    getIsFirstSession(state){
      return state.isFirstSession
    }
  },
  mutations: {
    setRole(state, role) {
      console.log("Setting role:", role);
      state.role = role;
      console.log("Set:", state.role);
    },
    setUserID(state, userID) {
      console.log("Setting userID:", userID);
      state.userID = userID;
      console.log("Set:", state.userID);
    },
    setIsFirstSession(state, isFirstSession) {
      console.log("Setting first session:", isFirstSession);
      state.isFirstSession = isFirstSession;
      console.log("Set:", state.isFirstSession);
    },
    removeUser(state) {
      console.log("Removing user details");
      state.role = null;
      state.userID = null;
      console.log("User details removed");
    },
  },
  actions: {
    logUser({ commit }, { role, user_id, is_first_session }) {
      commit("setRole", role);
      commit("setUserID", user_id);
      commit("setIsFirstSession", is_first_session);
    },
    logOut({ commit }) {
      commit("removeUser");
    },
  },
  modules: {
  }
});

