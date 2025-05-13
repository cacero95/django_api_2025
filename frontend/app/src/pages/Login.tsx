import { useContext, useRef } from "react"
import { Formik, Form, Field, ErrorMessage, FormikErrors } from "formik"
import { object, string } from "yup"
import Loader from '../assets/img/img/load.gif'
import { LoginForm } from "../interfaces/login-interface"
import { postLogin } from "../api/security/userRest"
import { AuthContext } from "../context/Auth/AuthContext"

const breadcumb6 = "../assets/img/bg-img/breadcumb6.jpg"

export const Login = () => {

    const { login, loading, setLoading, user } = useContext(AuthContext)
    console.log(user)
    const formRef = useRef<LoginForm>({ email: '', password: '' })
    const LoginSchema = object().shape({
        email: string()
            .email('Bad format')
            .required('Required'),
        password: string()
            .min(4, 'Bad format')
            .required('Required')
    })

    const validateForm = async (values: LoginForm) => {
        formRef.current = values
        setLoading(true);
        const { username, name, token, status } = await postLogin(values);
        status && login({ username, name, token })
        setLoading(false);
    }

    const validateDisable = (isSubmitting: boolean, isValid: boolean, errors: FormikErrors<LoginForm>, status: any) => {
        /**
         * errors: FormikErrors<LoginForm>
         * bring the error according the configuration
         */
        if (!isSubmitting) {
            return false
        }
        return !isValid && Object.keys(errors).length > 0
    }

    return (
        <div className="container text-center">
            <div 
                className = "breadcumb-area bg-img bg-overlay"
                style = {{ backgroundImage: `url(${breadcumb6})` }}
            >
                <div className="container h-100">
                    <div className="row h-100 align-items-center">
                        <div className="col-12">
                            <div className="breadcumb-text text-center">
                                <h2>Login</h2>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div className="contact-area section-pading-0-80">
                <div className="container text-center">
                    <div className="row">
                        <div className="col-12">
                            <div className="section-heading">
                                <h3>Ingresa tus datos</h3>
                            </div>
                        </div>
                    </div>
                    <div className="row" style={{ justifyContent: 'center' }}>
                        <div className="col-8">
                            <div className="contact-form-area">
                                <Formik
                                    initialValues = { formRef.current }
                                    validationSchema = { LoginSchema }
                                    onSubmit = { 
                                        ( values, { resetForm }) => {
                                            validateForm(values)
                                            resetForm();
                                        }
                                    }
                                >
                                    {
                                        ({ isSubmitting, isValid, errors, status }) => (
                                            <Form className = "space-y-4">
                                                <div className="row">
                                                    <div className="col-12 col-lg-12">
                                                        <ErrorMessage name="email" className="text text-danger" />
                                                        <Field type="text" name="email" className="form-control" placeholder="E-Mail:" />
                                                    </div>

                                                    <div className="col-12 col-lg-12">
                                                        <ErrorMessage name="password" className="text text-danger" />
                                                        <Field type="password" name="password" className="form-control" placeholder="Contraseña:" />
                                                    </div>

                                                    <div className="col-12 text-center" style={{ display: 'block' }}>
                                                        <button
                                                            className = "btn delicious-btn mt-30"
                                                            type = "submit"
                                                            title = "Sent"
                                                            disabled = { validateDisable(isSubmitting, isValid, errors, status) }
                                                        >
                                                            Enviar
                                                        </button>
                                                    </div>
                                                    <div className="col-12 text-center" style={{ display: loading ? 'block': 'none' }}>
                                                        <img src = { Loader } />
                                                    </div>

                                                </div>
                                            </Form>
                                        )
                                    }
                                </Formik>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    )
}
