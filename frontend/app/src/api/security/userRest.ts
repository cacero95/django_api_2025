import { LoginForm, LoginResponse } from "../../interfaces/login-interface"
import { back_api } from "../api"

export const postLogin = async (body: LoginForm): Promise<LoginResponse> => {
    try {
        const response = await fetch(`${ back_api }/users/login`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(body)
        })
        const data = await response.json() as LoginResponse
        return data.status === false ? { ...data, token: '' } : data
    } catch (err: any) {
        console.log(err)
        return {
            status: false,
            message: `${ err.message }`,
            token: '',
            username: '',
            name: ''
        }
    }
}