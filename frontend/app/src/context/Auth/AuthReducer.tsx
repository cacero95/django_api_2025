import { AuthState } from "./AuthContext"


type AuthOptions = {
    type: 'login' | 'closeSession' | 'handleLoading' | 'loading',
    payload: any
}

export const AuthReducer = ( state: AuthState, action: AuthOptions ): AuthState => {
    switch ( action.type ) {
        case 'login':
            return {
                ...state,
                user: action.payload
            }
        case "closeSession":
            return {
                ...state,
                user: null
            }
        case 'loading':
            return {
                ...state,
                loading: action.payload
            }
        default: return { ...state }
    }
}