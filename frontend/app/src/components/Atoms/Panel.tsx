import { FC } from 'react'
import { User } from '../../context/Auth/InitParameters'
import { Link } from 'react-router-dom'

interface Props {
    user: User
    closeSession: () => void
}

export const Panel: FC<Props> = ({ user, closeSession }) => (
    <>
        <Link to="/">Hola { user.username }</Link>
        <button onClick = { closeSession }>Close session</button>
    </>
)
