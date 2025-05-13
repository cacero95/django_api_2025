import { useRef, useEffect, useContext } from "react"
import { AuthContext } from "../context/Auth/AuthContext"
import { getRecipes } from "../api/recipes/recipesRest"
import { Datum } from "../interfaces/recipes"
import { Link } from "react-router-dom"

const breadcumb3 = '../assets/img/bg-img/breadcumb3.jpg'

export const Home = () => {

    const dataRef = useRef<Datum[]>([])
    const { setLoading } = useContext( AuthContext )

    const loadData = async () => {
        setLoading( true );
        const { data } = await getRecipes()
        dataRef.current = data
        setLoading( false );
    }

    useEffect(() => {
        loadData()
        // eslint-disable-next-line react-hooks/exhaustive-deps
    },[])

    return (
        <div>
            <div 
                className = "breadcumb-area bg-img bg-overlay"
                style = {{ backgroundImage: `url(${breadcumb3})` }}
            >
                <div className="container h-100">
                    <div className="row h-100 align-items-center">
                        <div className="col-12">
                            <div className="breadcumb-text text-center">
                                <h2>Recipes flaites - Development with React + Vite</h2>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <section className = "top-catagory-area section-padding-80-0">
                <div className="container"/>
            </section>

            <section className="best-receipe-area">
                <div className="container">

                    <div className="row">
                        <div className="col-12">
                            <div className="section-heading">
                                <h3>Últimas recetas publicadas </h3>
                            </div>
                        </div>
                    </div>

                    <div className="row">
                        {
                            dataRef.current.map(({ name, image, slug, id }) => (
                                <div className = "col-12 col-sm-6 col-lg-4" key = { id }>
                                    <div className = "single-best-receipe-area mb-30">
                                        <img src = { image } alt = { name } />
                                        <div className = "receipe-content">
                                            <Link to = { `recipe-detail/${ slug }` }>
                                                <h5>{ name }</h5>
                                            </Link>
                                        </div>
                                    </div>
                                </div>
                            ))
                        }
                    </div>

                </div>
            </section>
        </div>
    )
}
