
// SPDX-License-Identifier: MIT
pragma solidity 0.8.0;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol" ;
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";
//import "./test/ERC721.sol";
//import "../../chainlink/contracts/VRFConsumer.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {
    uint public tokenCounter ;
    bytes32 public keyhash ;
    uint256 public fee ;
    enum Breed{PUG, SHIBA_INU, ST_BERNARD}
    mapping(uint256 => Breed) public tokenIdToBreed ;
    mapping(bytes32 => address) public requestIdToSender ;
    event requestCollectible(bytes32 indexed requestId, address requester) ;
    event breedAssigned(uint256 indexed tokenId, Breed breed) ;
    mapping (uint256 => string) private _tokenURIs;

    constructor(
        address _vrfCoordinator, address _linkToken, bytes32 _keyhash, uint256 _fee
    ) public VRFConsumerBase(_vrfCoordinator, _linkToken) ERC721("Dogie", "DOG"){
        tokenCounter = 0 ;
        keyhash = _keyhash ;
        fee = _fee ;
    }

    function createCollectible() public returns (bytes32){
        bytes32 requestId = requestRandomness(keyhash, fee) ;
        requestIdToSender[requestId] = msg.sender ;
        emit requestCollectible(requestId, msg.sender) ;
        return requestId ;
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override {
//    function fulfilRandomness(bytes32 requestId, uint256 randomNumber) internal {
//    function fulfilRandomness(bytes32 requestId, uint256 randomNumber) internal abstract {
        Breed breed = Breed(randomNumber % 3) ;
        uint256 newTokenId = tokenCounter ;
        tokenIdToBreed[newTokenId] = breed ;
        emit breedAssigned(newTokenId, breed) ;
        address owner = requestIdToSender[requestId] ;
        _safeMint(owner, newTokenId) ;
        tokenCounter = tokenCounter + 1;
    }

    // Added my CCCXN based on https://forum.openzeppelin.com/t/function-settokenuri-in-erc721-is-gone-with-pragma-0-8-0/5978/14
    function _setTokenURI(uint256 tokenId, string memory _tokenURI) internal virtual {
        require(_exists(tokenId), "ERC721Metadata: URI set of nonexistent token");
        _tokenURIs[tokenId] = _tokenURI;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(_isApprovedOrOwner(_msgSender(), tokenId), "ERC721: caller is not owner no approved ") ;
        _setTokenURI(tokenId, _tokenURI) ;
    }






}