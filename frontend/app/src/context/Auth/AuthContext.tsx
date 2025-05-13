import { createContext, useReducer } from "react";
import { getUser, type User } from "./InitParameters";
import { AuthReducer } from "./AuthReducer";

export interface AuthState {
    user: User | any
    loading: boolean
}

export interface AuthPropsContext {
    user: User
    loading: boolean
    login: ( auth : User ) => void
    logout: () => void
    setLoading: ( value: boolean ) => void
}

export const initAuth: AuthState = {
    user: getUser(),
    loading: false
}

export const AuthContext = createContext( {} as AuthPropsContext )

export const AuthProvider = ({ children }: any) => {
    
    const [ authState, dispatch ] = useReducer( AuthReducer, initAuth )

    const setLoading = (value: boolean) => dispatch({ type: 'loading', payload: value })

    const login = ( payload: User ) => dispatch({ type: "login", payload })

    const logout = () => dispatch({ type: "closeSession", payload: null })

    return (
        <AuthContext.Provider
            value = {{
                ...authState,
                login,
                logout,
                setLoading
            }}
        >
            { children }
        </AuthContext.Provider>
    )
}