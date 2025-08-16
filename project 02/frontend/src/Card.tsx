import { useContext } from "react";
import { UserContext } from "./UserContext";

interface Shipment {
    id: string
    status: string
}

function Card({ shipment }: { shipment: Shipment }) {

    return (
        <div className="card">
            <h2>Status: {shipment.status}</h2>
            <p>Id #{shipment.id}</p>
        </div>
    );
}

export { Card, type Shipment }