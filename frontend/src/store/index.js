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
    }
  },
  actions: {
    logUser({ commit }, { role, userID, isFirstSession }) {
      commit("setRole", role);
      commit("setUserID", userID);
      commit("setIsFirstSession", isFirstSession);
    }
  },
  modules: {
  }
});

