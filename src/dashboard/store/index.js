
export const getters = {
    isAuthenticated(state) {
      return state.auth.loggedIn
    },
  
    loggedInUser(state) {
      return state.auth.user
    }
}

// export const mutations = {
//   // Define mutations to modify the state
//   setData(state, payload) {
//     state.auth.user = payload;
//   },
// }

// export const actions = {
//   async storeLoggedUser({ state, loggedUser }) {
//     // state.auth.user = loggedUser;

//     commit('setData', loggedUser);
//   }
// }