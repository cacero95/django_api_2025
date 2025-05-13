import { Recipes } from "../../interfaces/recipes"
import { back_api } from "../api"

export const getRecipes = async (): Promise<Recipes> => {
    try {
        const response = await fetch(`${ back_api }/user_recipe`)
        const data = await response.json() as Recipes;
        return data.status === false ? { ...data, data: [] } : data
    } catch(err: any) {
        console.log(err)
        return {
            data: [],
            status: false,
            message: err.message
        }
    }
}