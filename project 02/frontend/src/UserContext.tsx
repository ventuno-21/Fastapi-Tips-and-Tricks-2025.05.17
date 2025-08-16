import { createContext, ReactNode, useState } from "react";

interface UserContextType {
    username: string | null
    login: (name: string) => void
    logout: () => void
}

const UserContext = createContext<UserContextType>({
    username: null,
    login: () => { },
    logout: () => { }
})


function UserProvider(
    { children }: { children: ReactNode }
) {
    const [username, setUsername] = useState<string | null>(null)

    function login(name: string) {
        setUsername(name)
    }

    return (
        <UserContext.Provider value={
            {
                username,
                login,
                logout: () => setUsername(null)
            }
        }>
            {children}
        </UserContext.Provider>
    )
}

export { UserProvider, UserContext }