import { FC } from 'react'
import { Header } from '../shared/Header'
import { Footer } from '../shared/Footer'

interface Props {
    component: any
}

export const Container: FC<Props> = ({ component }) => {
    return (
        <div>
            <Header />
            { component }
            <Footer />
        </div>
    )
}
