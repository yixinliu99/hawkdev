import React, {useEffect, useState} from 'react';
import {Button, Card, Col, Container, Form, Modal, Row} from 'react-bootstrap';
import {useNavigate, useParams} from 'react-router-dom';
import config from '../config';

const convertDateToLocalISOString = (date) => {
    const pad = num => num.toString().padStart(2, '0'); // Ensures two digits
    return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`;
}

const CreateAuctionForm = ({showModal, handleCloseModal, itemId, userId}) => {
    const [auctionDetails, setAuctionDetails] = useState({
        startingPrice: 100,
        startingTime: convertDateToLocalISOString(new Date()),
        endingTime: convertDateToLocalISOString(new Date(Date.now() + 1000 * 60 * 60 * 24)), // 24 hours from now
        buyNowPrice: 0,
    });

    const handleFormSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch(`${config.AUCTION_SERVICE_URL}/auctions/create`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                body: JSON.stringify({
                    starting_price: auctionDetails.startingPrice,
                    starting_time: new Date(auctionDetails.startingTime).toISOString(),
                    ending_time: new Date(auctionDetails.endingTime).toISOString(),
                    seller_id: userId,
                    item_id: itemId,
                    buy_now_price: auctionDetails.buyNowPrice,
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to create auction');
            }

            const updatedItem = await response.json();
            // Handle the updated item (for example, updating the items list)
            handleCloseModal();
        } catch (error) {
            console.error('Failed to create auction', error);
        }
    };

    return (
        <Modal show={showModal} onHide={handleCloseModal}>
            <Modal.Header closeButton>
                <Modal.Title>Create Auction</Modal.Title>
            </Modal.Header>
            <Modal.Body>
                <Form onSubmit={handleFormSubmit}>
                    <Form.Group controlId="startingPrice">
                        <Form.Label>Starting Price</Form.Label>
                        <Form.Control
                            type="number"
                            step="0.01"
                            min="0"
                            value={auctionDetails.startingPrice}
                            onChange={(e) =>
                                setAuctionDetails({...auctionDetails, startingPrice: e.target.value})
                            }
                            required
                        />
                    </Form.Group>

                    <Form.Group controlId="startingTime">
                        <Form.Label>Starting Time</Form.Label>
                        <Form.Control
                            type="datetime-local"
                            value={auctionDetails.startingTime}
                            onChange={(e) =>
                                setAuctionDetails({...auctionDetails, startingTime: e.target.value})
                            }
                            required
                        />
                    </Form.Group>

                    <Form.Group controlId="endingTime">
                        <Form.Label>Ending Time</Form.Label>
                        <Form.Control
                            type="datetime-local"
                            value={auctionDetails.endingTime}
                            onChange={(e) =>
                                setAuctionDetails({...auctionDetails, endingTime: e.target.value})
                            }
                            required
                        />
                    </Form.Group>

                    <Form.Group controlId="buyNowPrice">
                        <Form.Label>Buy Now Price</Form.Label>
                        <Form.Control
                            type="number"
                            step="0.01"
                            min="0"
                            value={auctionDetails.buyNowPrice}
                            onChange={(e) =>
                                setAuctionDetails({...auctionDetails, buyNowPrice: e.target.value})
                            }
                        />
                    </Form.Group>


                    <Button variant="primary" type="submit" className="mt-3">
                        Create Auction
                    </Button>
                </Form>
            </Modal.Body>
            <Modal.Footer>
                <Button variant="secondary" onClick={handleCloseModal}>
                    Cancel
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

const Bidding = () => {
    const [items, setItems] = useState([]);
    const [showModal, setShowModal] = useState(false);
    const [selectedItem, setSelectedItem] = useState(null);
    const navigate = useNavigate();
    const {user_id} = useParams();

    const handleCloseModal = () => setShowModal(false);
    const handleShowModal = (item) => {
        setSelectedItem(item);
        setShowModal(true);
    };

    useEffect(() => {
        const fetchItems = async () => {
            try {
                const response = await fetch(`${config.ITEM_SERVICE_URL}/items`);
                const data = await response.json();
                setItems(data);
            } catch (error) {
                console.error('Failed to fetch items', error);
            }
        };

        fetchItems();
    }, []);

    return (
        <Container className="mt-4">
            <h2 className="mb-4">Items</h2>
            <Row>
                {items.length === 0 ? (
                    <Col>
                        <p>No items available</p>
                    </Col>
                ) : (
                    items.map((item) => (
                        <Col key={item._id} md={4} className="mb-4">
                            <Card className="h-100">
                                <Card.Body>
                                    <Card.Title>{item.description}</Card.Title>
                                    <Card.Text>
                                        <strong>Category:</strong> {item.category}
                                        <br/>
                                        <strong>Keywords:</strong> {item.keywords.join(', ')}
                                        <br/>
                                        <strong>Starting Price:</strong> ${item.starting_price}
                                    </Card.Text>
                                    {item.auction_id ? (
                                        <Button
                                            variant="success"
                                            onClick={() => navigate(`/bid/${item._id}`)}
                                        >
                                            Place Bid
                                        </Button>
                                    ) : (
                                        <Button
                                            variant="primary"
                                            onClick={() => handleShowModal(item)}
                                        >
                                            Create Auction
                                        </Button>
                                    )}
                                </Card.Body>
                            </Card>
                        </Col>
                    ))
                )}
            </Row>

            {/* Modal for creating auction */}
            {selectedItem && (
                <CreateAuctionForm
                    showModal={showModal}
                    handleCloseModal={handleCloseModal}
                    itemId={selectedItem._id}
                    userId={user_id}
                />
            )}
        </Container>
    );
};

export default Bidding;
